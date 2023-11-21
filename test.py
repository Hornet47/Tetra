from agents import Agent
from openai import OpenAI
import user_proxy
import utils
import json

config_file_path = 'assistant_config.json'

with open(config_file_path, 'r') as file:
    config = json.load(file)
    
client = OpenAI()

code_writer = Agent(
    **config["PostgreSQL_writer"]
)
msg = code_writer.process_message("Generate the query for: the most popular film category in China")
query = utils.extract_sql(msg)
print(query)
res = user_proxy.run_sql(query=query)
print(res)