from openai import OpenAI
from team.managers import Manager
from agent import utils

def main():
    client = OpenAI()
    manager: Manager = Manager.get_or_create(client=client, team_name="data_analytics_team")
    
if __name__ == "__main__":
    main()