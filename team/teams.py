from agent.agents import Agent
from typing import List
import json

class Team:
    with open('team/team_config.json', 'r') as file:
        team_config = json.load(file)
        
    with open('agent/agent_config.json', 'r') as file:
        agent_config = json.load(file)
    
    def __init__(self, name: str):
        self.members: List[Agent] = []
        for agent_name in Team.team_config[name]:
            self.members.append(Agent(**Team.agent_config[agent_name]))