from openai import OpenAI
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run
from openai.types.beta.assistant_create_params import Tool
from typing import List, Dict
from time import sleep
from agent import toolcalls


class Agent:
    client = OpenAI()

    def __init__(
        self,
        model: str = "gpt-3.5-turbo-1106",
        name: str = "Assistant",
        instructions: str = "You are a helpful assistant.",
        tools: List[Tool] = [],
        file_names: List[str] = [],
    ):
        self.name = name
        self.id = None
        
        print(f"Creating Agent {self.name}...")
        # Check if there is an Assistant with the same name. If not, create one.
        assistants = Agent.client.beta.assistants.list().data
        for assistant in assistants:
            if assistant.name == name:
                print(f"{name} already exists.")
                self.id = assistant.id
                break

        if self.id is None:
            self.id = Agent.client.beta.assistants.create(model=model).id

        file_ids = Agent.get_or_create_files(file_names=file_names)

        Agent.client.beta.assistants.update(
            self.id, model=model, instructions=instructions, tools=tools, file_ids=file_ids
        )
        self.threads: Dict[str, Thread] = {}

    def get_or_create_files(file_names: List[str]):
        
        file_ids = []

        for file_name in file_names:
            print(f"Uploading {file_name}...")
            exist = False
            for data in Agent.client.files.list().data:
                if data.filename == file_name:
                    file_ids.append(data.id)
                    exist = True
                    print(f"{file_name} already exists.")
                    break
            if not exist:
                file = Agent.client.files.create(
                    file=open(f"files/{file_name}", "rb"), purpose="assistants"
                )
                file_ids.append(file.id)
        return file_ids

    def submit_tool_outputs(self, run: Run, thread: Thread):
        
        if run.status != "requires_action":
            return
        
        _toolcalls = run.required_action.submit_tool_outputs.tool_calls
        outputs = toolcalls.execute_all(_toolcalls)
        print("Submitting tool outputs...")
        Agent.client.beta.threads.runs.submit_tool_outputs(
            run_id=run.id, thread_id=thread.id, tool_outputs=outputs
        )

    def process_message(
        self,
        message: str,
        thread_name: str = "new thread",
        file_names: List[str] = [],
    ) -> str:
        
        # create a new thread if thread name doesn't exist
        thread = (
            Agent.client.beta.threads.create()
            if thread_name not in self.threads
            else self.threads[thread_name]
        )
        
        # add thread-specific files
        file_ids = Agent.get_or_create_files(file_names=file_names)
        if file_ids.__len__() != 0:
            Agent.client.beta.threads.messages.create(
                thread_id=thread.id, file_ids=file_ids, role="user"
            )

        Agent.client.beta.threads.messages.create(
            thread_id=thread.id, content=message, role="user"
        )
        run: Run = Agent.client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=self.id
        )
        
        # wait for the run to complete
        print(f"{self.name} is processing message...")
        while True:
            run = Agent.client.beta.threads.runs.retrieve(
                run_id=run.id, thread_id=thread.id
            )
            if run.status == "requires_action":
                self.submit_tool_outputs(run, thread)
            elif run.status == "completed":
                return (
                    Agent.client.beta.threads.messages.list(thread.id)
                    .data[0]
                    .content[0]
                    .text.value
                )
            elif run.status == "failed":
                print(run.last_error)
                break
            sleep(0.5)
