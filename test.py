from tetras import Tetra
import functions
from openai import OpenAI
import json

config_file_path = 'assistant_config.json'

with open(config_file_path, 'r') as file:
    config = json.load(file)
    
client = OpenAI().beta

code_writer = Tetra(
    client=client,
    **config["code_writer"]
)
msg = code_writer.process_message("Generate the python script that draw a 3d surface of x**2+y**2.")
file_name, code = functions.extract_code(msg)
functions.write_into_file(file_name, code)
functions.execute(file_name)