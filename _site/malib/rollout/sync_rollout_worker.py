import ray

from malib.rollout.rollout_worker import RolloutWorker
from malib.utils.typing import (
    TaskDescription,
    Status,
    RolloutDescription,
    Any,
    Dict,
    BufferDescription,
)


class SyncRolloutWorker(RolloutWorker):
    def __init__(
        self,
        worker_index: str,
        env_desc: Dict[str, Any],
        metric_type: str,
        remote: bool = False,
        **kwargs
    ):
        """Create a rollout worker instance.

        :param str worker_index: Indicate rollout worker
        :param Dict[str,Any] env_desc: The environment description
        :param str metric_type: Name of registered metric handler
        :param bool remote: Tell this rollout worker work in remote mode or not, default by False
        """

        RolloutWorker.__init__(
            self, worker_index, env_desc, metric_type, remote, **kwargs
        )

    def update_state(self, task_desc: TaskDescription, waiting=False) -> Status:
        wait_list = {
            aid: pid
            for aid, (
                pid,
                _,
            ) in task_desc.content.agent_involve_info.trainable_pairs.items()
        }
        if isinstance(task_desc.content, RolloutDescription):
            status = Status.FAILED
            while status == Status.FAILED:
                status = ray.get(
                    self._offline_dataset.lock.remote(
                        lock_type="push",
                        desc={
                            agent: BufferDescription(
                                env_id=self._env_description["id"],
                                agent_id=agent,
                                policy_id=pid,
                            )
                            for agent, pid in wait_list.items()
                        },
                    )
                )
                tmp = Status.SUCCESS
                ks = list(status.keys())
                for k in ks:
                    v = status[k]
                    if v == Status.SUCCESS:
                        wait_list.pop(k)
                    elif v == Status.FAILED:
                        tmp = Status.FAILED
                status = tmp
            assert status == Status.SUCCESS, status
        return RolloutWorker.update_state(self, task_desc, waiting)

    def after_rollout(self, trainable_pairs):
        """Define behavior after one rollout iteration. Here we unlock the pushing process and transfer the access
        rights to synchronous training agent interfaces.

        :param Dict[AgentID,Tuple[Policy,Any]] trainable_pairs: Training policy configuration.
        """

        # unlock
        ray.get(
            self._offline_dataset.unlock.remote(
                lock_type="push",
                desc={
                    agent: BufferDescription(
                        env_id=self._env_description["id"],
                        agent_id=agent,
                        policy_id=pid,
                    )
                    for agent, (
                        pid,
                        _,
                    ) in trainable_pairs.items()
                },
            )
        )
