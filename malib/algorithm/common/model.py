"""
Model factory. Add more description
"""

import copy
from typing import Optional

import gym
import torch
import torch.nn as nn
import torch.nn.functional as F

from malib.utils.preprocessor import Mode, get_preprocessor
from malib.utils.typing import DataTransferType, Dict, Any, List


def mlp(layers_config):
    layers = []
    for j in range(len(layers_config) - 1):
        tmp = [nn.Linear(layers_config[j]["units"], layers_config[j + 1]["units"])]
        if layers_config[j + 1].get("activation"):
            tmp.append(getattr(torch.nn, layers_config[j + 1]["activation"])())
        layers += tmp
    return nn.Sequential(*layers)


class Model(nn.Module):
    def __init__(self, input_space, output_space):
        """
        Create a Model instance.
        Common abstract methods could be added here.

        :param input_space: Input space size, int or gym.spaces.Space.
        :param output_space: Output space size, int or gym.spaces.Space.
        """

        super(Model, self).__init__()
        if isinstance(input_space, gym.spaces.Space):
            self.input_dim = get_preprocessor(input_space)(input_space).size
        else:
            self.input_dim = input_space

        if isinstance(output_space, gym.spaces.Space):
            self.output_dim = get_preprocessor(output_space)(output_space).size
        else:
            self.output_dim = output_space

    def get_initial_state(
        self, batch_size: Optional[int] = None
    ) -> List[torch.TensorType]:
        """Return a list of initial rnn state, if current model is rnn"""

        return []


class MLP(Model):
    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        model_config: Dict[str, Any],
        **kwargs
    ):
        super(MLP, self).__init__(observation_space, action_space)

        layers_config: list = (
            self._default_layers()
            if model_config.get("layers") is None
            else model_config["layers"]
        )
        layers_config.insert(0, {"units": self.input_dim})

        if action_space:
            act_dim = get_preprocessor(action_space)(action_space).size
            layers_config.append(
                {"units": act_dim, "activation": model_config["output"]["activation"]}
            )
        self.use_feature_normalization = kwargs.get("use_feature_normalization", False)
        if self.use_feature_normalization:
            self._feature_norm = nn.LayerNorm(self.input_dim)
        self.net = mlp(layers_config)

    def _default_layers(self):
        return [
            {"units": 256, "activation": "ReLU"},
            {"units": 64, "activation": "ReLU"},
        ]

    def forward(self, obs):
        obs = torch.as_tensor(obs, dtype=torch.float32)
        if self.use_feature_normalization:
            obs = self._feature_norm(obs)
        pi = self.net(obs)
        return pi


class RNN(Model):
    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        model_config: Dict[str, Any],
    ):
        super(RNN, self).__init__(observation_space, action_space)
        self.hidden_dim = (
            64 if model_config is None else model_config.get("rnn_hidden_dim", 64)
        )

        # default by flatten
        self.fc1 = nn.Linear(self.input_dim, self.hidden_dim)
        self.rnn = nn.GRUCell(self.hidden_dim, self.hidden_dim)
        self.fc2 = nn.Linear(self.hidden_dim, self.output_dim)

    def _init_hidden(self, batch_size: Optional[int] = None):
        # make hidden states on same device as model
        if batch_size is None:
            batch_size = 1
        return self.fc1.weight.new(batch_size, self.hidden_dim).zero_()

    def get_initial_state(
        self, batch_size: Optional[int] = None
    ) -> List[torch.TensorType]:
        return [self._init_hidden(batch_size)]

    def forward(self, obs, hidden_state):
        obs = torch.as_tensor(obs, dtype=torch.float32)

        x = F.relu(self.fc1(obs))
        h_in = hidden_state.reshape(-1, self.hidden_dim)
        h = self.rnn(x, h_in)
        q = self.fc2(h)
        return q, h


def get_model(model_config: Dict[str, Any]):
    model_type = model_config["network"]

    if model_type == "mlp":
        handler = MLP
    elif model_type == "rnn":
        handler = RNN
    elif model_type == "cnn":
        raise NotImplementedError
    elif model_type == "rcnn":
        raise NotImplementedError
    else:
        raise NotImplementedError

    def builder(observation_space, action_space, use_cuda=False, **kwargs):
        model = handler(
            observation_space, action_space, copy.deepcopy(model_config), **kwargs
        )
        if use_cuda:
            model.cuda()
        return model

    return builder
