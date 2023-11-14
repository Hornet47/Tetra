from openai.resources import Beta
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run
from openai.types.beta.assistant_create_params import Tool
from typing import List, Dict
from time import sleep
import toolcalls

class Tetra:
    def __init__(
        self,
        client: Beta,
        model: str = "gpt-3.5-turbo-1106",
        name: str = "Assistant",
        instructions: str = "You are a helpful assistant.",
        tools: List[Tool] = [],
        ):
        self.client = client
        self.name = name
        self.id = None
        #Check if there is an Assistant with the same name. If not, create one.
        assistants = self.client.assistants.list().data
        for assistant in assistants:
            if assistant.name == name:
                self.id = assistant.id
                break
        
        if self.id is None:
            self.id = self.client.assistants.create(model=model).id
        
        self.client.assistants.update(self.id, instructions=instructions, tools=tools)
        self.threads: Dict[str, Thread] = {}
        
        
    def submit_tool_outputs(self, run: Run, thread: Thread):
        _toolcalls = run.required_action.submit_tool_outputs.tool_calls
        outputs = toolcalls.execute_all(_toolcalls)
        self.client.threads.runs.submit_tool_outputs(
            run_id=run.id, 
            thread_id=thread.id, 
            tool_outputs=outputs
            )
        
    def process_message(
        self,
        message: str,
        thread_name: str = "new thread",\
        ) -> str:
        thread = self.client.threads.create() if thread_name not in self.threads else self.threads[thread_name]
        self.client.threads.messages.create(thread_id=thread.id, content=message, role = "user")
        run: Run = self.client.threads.runs.create(thread_id=thread.id, assistant_id=self.id)
        while True:
            run = self.client.threads.runs.retrieve(run_id=run.id, thread_id=thread.id)
            if run.status == "requires_action":
                self.submit_tool_outputs(run, thread)
            elif run.status == "completed":
                return self.client.threads.messages.list(thread.id).data[0].content[0].text.value
            sleep(0.5)