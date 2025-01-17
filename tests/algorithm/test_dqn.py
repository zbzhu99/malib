from typing import Dict
from malib.utils.episode import EpisodeKey
from tests.algorithm import AlgorithmTestMixin
from gym import spaces
import numpy as np
from malib.algorithm.dqn import CONFIG, DQN, DQNTrainer, DQNLoss
from malib.algorithm.dqn.conv import DuelQNet
import torch

trainer_config = CONFIG["training"]
custom_config = CONFIG["policy"]

model_config = {
    "critic": {
        "network": "mlp",
        "layers": [{"units": 64, "activation": "ReLU"}],
        "output": {"activation": False},
    }
}

test_obs_shape = (3,)
test_action_dim = 2


class TestDQN(AlgorithmTestMixin):
    def make_algorithm(self, *args):
        return DQN(
            registered_name="DQN",
            observation_space=spaces.Box(low=0, high=1, shape=test_obs_shape),
            action_space=spaces.Discrete(n=test_action_dim),
            model_config=model_config,
            custom_config=custom_config,
        )

    def make_trainer_and_config(self):
        return DQNTrainer("test_trainer"), trainer_config

    def make_loss(self):
        return DQNLoss()

    def build_env_inputs(self) -> Dict:
        return {
            EpisodeKey.CUR_OBS: np.zeros((1,) + test_obs_shape),
            EpisodeKey.RNN_STATE: self.algorithm.get_initial_state(1),
        }

    def build_train_inputs(self) -> Dict:
        batch_size = 32
        action_mask = np.zeros((batch_size, test_action_dim))
        action_mask[:, 0] = 1
        return {
            EpisodeKey.CUR_OBS: np.zeros((batch_size,) + test_obs_shape),
            EpisodeKey.NEXT_OBS: np.zeros((batch_size,) + test_obs_shape),
            EpisodeKey.ACTION: np.zeros((batch_size, 1)),
            EpisodeKey.DONE: np.zeros((batch_size, 1)),
            EpisodeKey.REWARD: np.zeros((batch_size, 1)),
            "next_action_mask": action_mask,
        }

    def test_conv_dqn(self):
        """Test conv DQN network."""
        net = DuelQNet(input_shape=(4, 84, 84), available_actions_count=3)

        input_data = torch.zeros((5, 4, 84, 84))
        output = net(input_data)
        assert list(output.shape) == [5, 3]
