from tetras import Tetra
import functions
from openai import OpenAI

client = OpenAI().beta
code_writer = Tetra(
    client=client,
    name="code_writer",
    instructions=
    "You are an experienced python programmer. You will generate python scripts based on my requests and return it to me as string. You can use useful python packages. Do not execute the script. Do not ask me if you should generate python script, just generate it directly.",
    tools=[
        {
            "type": "code_interpreter",
        },
    ]
)
msg = code_writer.process_message("Generate the python script that draw a 3d surface of x**2+y**2.")
content = functions.extract_section(msg, "```python", "```")
functions.write_into_file("draw.py", content)