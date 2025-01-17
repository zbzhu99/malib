import importlib
import pytest
import ray
from malib.utils.episode import NewEpisodeDict, Episode

from malib.utils.typing import BufferDescription
from malib.envs import Environment
from malib.envs.vector_env import VectorEnv
from malib.rollout.rollout_func import (
    env_runner,
    _do_policy_eval,
    _process_policy_outputs,
    _process_environment_returns,
)

from tests.env_api.utils import build_dummy_agent_interfaces
from tests.dataset.utils import FakeDataServer


@pytest.mark.parametrize(
    "module_path,cname,config,batch_mode",
    [
        (
            "malib.envs.poker",
            "PokerParallelEnv",
            {"env_id": "leduc_poker", "scenario_configs": {"fixed_player": True}},
            "time_step",
        ),
        (
            "malib.envs.gym",
            "GymEnv",
            {"env_id": "CartPole-v0", "scenario_configs": {}},
            "time_step",
        ),
        (
            "malib.envs.mpe",
            "MPE",
            {"env_id": "simple_push_v2", "scenario_configs": {"max_cycles": 25}},
            "time_step",
        ),
        (
            "malib.envs.mpe",
            "MPE",
            {"env_id": "simple_spread_v2", "scenario_configs": {"max_cycles": 25}},
            "time_step",
        ),
        (
            "malib.envs.gr_football",
            "creator",
            {
                "env_id": "Gfootball",
                "scenario_configs": {
                    "env_name": "5_vs_5",
                    "number_of_left_players_agent_controls": 4,
                    "number_of_right_players_agent_controls": 4,
                    "representation": "raw",
                    "logdir": "",
                    "write_goal_dumps": False,
                    "write_full_episode_dumps": False,
                    "render": False,
                    "stacked": False,
                },
            },
            "episode",
        ),
        (
            "malib.envs.maatari",
            "MAAtari",
            {
                "env_id": "basketball_pong_v2",
                "wrappers": [
                    {"name": "resize_v0", "params": [84, 84]},
                    {"name": "dtype_v0", "params": ["float32"]},
                    {
                        "name": "normalize_obs_v0",
                        "params": {"env_min": 0.0, "env_max": 1.0},
                    },
                ],
                "scenario_configs": {
                    "obs_type": "grayscale_image",
                    "num_players": 2,
                },
            },
            "time_step",
        ),
    ],
    scope="class",
)
class TestEnvRunner:
    @pytest.fixture(autouse=True)
    def _init(self, module_path, cname, config, batch_mode):
        if not ray.is_initialized():
            ray.init(local_mode=True)
        creator = getattr(importlib.import_module(module_path), cname)
        env: Environment = creator(**config)

        observation_spaces = env.observation_spaces
        action_spaces = env.action_spaces

        vec_env = VectorEnv(
            observation_spaces,
            action_spaces,
            creator,
            configs=config,
        )

        agent_interfaces = build_dummy_agent_interfaces(
            observation_spaces, action_spaces
        )

        self.vec_env = vec_env
        self.agent_interfaces = agent_interfaces

        self.vec_env.add_envs(num=4)
        self.batch_mode = batch_mode
        self.observation_spaces = observation_spaces
        self.action_spaces = action_spaces

    def test_process_in_runner(self):
        runtime_config = {
            "num_envs": 2,
            "fragment_length": 100,
            "max_step": 25,
            "custom_reset_config": None,
            "batch_mode": self.batch_mode,
            "postprocessor_types": ["default"],
            "trainable_mapping": None,
        }
        _ = [interface.reset() for interface in self.agent_interfaces.values()]
        rets = self.vec_env.reset(
            limits=runtime_config["num_envs"],
            fragment_length=runtime_config["fragment_length"],
            max_step=runtime_config["max_step"],
            custom_reset_config=runtime_config["custom_reset_config"],
        )

        behavior_policies = {
            aid: interface.behavior_policy
            for aid, interface in self.agent_interfaces.items()
        }

        episodes = NewEpisodeDict(
            lambda env_id: Episode(behavior_policies, env_id=env_id)
        )

        while not self.vec_env.is_terminated():
            filtered_outputs = {}
            policy_inputs, filtered_outputs, _ = _process_environment_returns(
                env_rets=rets,
                agent_interfaces=self.agent_interfaces,
                filtered_env_outputs=filtered_outputs,
            )

            # check consistency in env ids
            pinput_env_ids = sorted(list(policy_inputs.keys()))
            filtered_env_ids = sorted(list(filtered_outputs.keys()))
            real_env_ids = sorted(list(self.vec_env.active_envs.keys()))

            # assert pinput_env_ids == filtered_env_ids == real_env_ids, (
            #     pinput_env_ids,
            #     filtered_env_ids,
            #     real_env_ids,
            # )

            policy_outputs, active_env_ids = _do_policy_eval(
                policy_inputs, self.agent_interfaces, episodes
            )
            sorted_active_env_ids = sorted(active_env_ids)
            assert sorted_active_env_ids == pinput_env_ids

            env_inputs, detached_policy_outputs = _process_policy_outputs(
                active_env_ids, policy_outputs, self.vec_env
            )

            rets = self.vec_env.step(env_inputs)

            policy_inputs, filtered_outputs, _ = _process_environment_returns(
                env_rets=rets,
                agent_interfaces=self.agent_interfaces,
                filtered_env_outputs=filtered_outputs,
            )

            detached_env_ids = sorted(detached_policy_outputs.keys())
            assert sorted_active_env_ids == detached_env_ids, (
                sorted_active_env_ids,
                detached_env_ids,
            )

            episodes.record(detached_policy_outputs, filtered_outputs)

    def test_env_runner_no_buffer_send(self):
        # random select agent behavior policies
        _ = [interface.reset() for interface in self.agent_interfaces.values()]
        behavior_policy_ids = {
            agent_id: interface.behavior_policy
            for agent_id, interface in self.agent_interfaces.items()
        }
        rollout_info = env_runner(
            self.vec_env,
            self.agent_interfaces,
            buffer_desc=None,
            runtime_config={
                "max_step": 10,
                "num_envs": 2,
                "fragment_length": 100,
                "behavior_policies": behavior_policy_ids,
                "custom_reset_config": None,
                "batch_mode": self.batch_mode,
                "postprocessor_types": ["default"],
                "trainable_mapping": None,
            },
            dataset_server=None,
        )

    def test_env_runner_with_buffer_send(self):
        _ = [interface.reset() for interface in self.agent_interfaces.values()]
        behavior_policy_ids = {
            agent_id: interface.behavior_policy
            for agent_id, interface in self.agent_interfaces.items()
        }
        dataset = FakeDataServer.remote()
        buffer_desc = BufferDescription(
            env_id=self.vec_env.env_configs["env_id"],
            agent_id=self.vec_env.possible_agents,
            policy_id=[
                behavior_policy_ids[aid] for aid in self.vec_env.possible_agents
            ],
        )

        rollout_info = env_runner(
            self.vec_env,
            self.agent_interfaces,
            buffer_desc=buffer_desc,
            runtime_config={
                "max_step": 10,
                "num_envs": 2,
                "fragment_length": 100,
                "behavior_policies": behavior_policy_ids,
                "custom_reset_config": None,
                "batch_mode": self.batch_mode,
                "postprocessor_types": ["default"],
                "trainable_mapping": behavior_policy_ids,
            },
            dataset_server=dataset,
        )
