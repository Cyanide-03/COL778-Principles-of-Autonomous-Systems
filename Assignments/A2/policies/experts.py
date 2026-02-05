
import os
import torch
import torch.nn as nn
import utils.utils as utils
from agents.base_agent import BaseAgent
import utils.pytorch_util as ptu



class ExpertPolicy(nn.Module):
    def __init__(self, observation_dim, action_dim, num_layers, hidden_size) -> None:
        super().__init__()
        self.total_calls = 0
        self.policy = ptu.build_mlp(observation_dim, action_dim, num_layers, hidden_size)

    def forward(self, observation):
        return self.policy(observation)
    
    @torch.no_grad()
    def get_action(self, observation):
        self.total_calls+=1
        action  = self.forward(observation)
        action = action.detach().cpu().numpy()
        return action
    

class ExpertPolicyJIT(nn.Module):
    def __init__(self, policy):
        super().__init__()
        self.policy = policy
        self.policy.eval()

    def forward(self, observation):
        if observation.dim() == 1:
            observation = observation.unsqueeze(0)
        return self.policy(observation)

    @torch.no_grad()
    def get_action(self, observation):
        if observation.dim() == 1:
            observation = observation.unsqueeze(0)

        action = self.policy(observation)
        return action.squeeze(0).cpu().numpy()


def load_expert_policy(env, env_name, jit=True):
    if not jit:
        state_dict =  torch.load(os.path.join("./policies/experts", env_name + ".pth"))
        state_dict = {"policy."+k :v for k,v in state_dict.items()}
        expert_policy = ExpertPolicy(env.observation_space.shape[0], env.action_space.shape[0], len(state_dict)//2 -1, state_dict['policy.0.weight'].shape[0])

        expert_policy.load_state_dict(state_dict)
        expert_policy.to(ptu.device)
    else:
        expert_policy = torch.jit.load(os.path.join("./policies/experts", env_name + "_jit.pt"), map_location=ptu.device)
        expert_policy = ExpertPolicyJIT(expert_policy)
    return expert_policy



