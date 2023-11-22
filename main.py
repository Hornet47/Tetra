from agent.agents import Agent
from agent import user_proxy, utils
import json

def main():
    with open('agent/agent_config.json', 'r') as file:
        config = json.load(file)

    code_writer = Agent(
        **config["postgreSQL_writer"]
    )
    msg = code_writer.process_message("Generate the query for: which film category has the highest average price?")
    query = utils.extract_sql(msg)
    print(query)
    res = user_proxy.run_sql(query=query)
    print(res)
    
if __name__ == "__main__":
    main()