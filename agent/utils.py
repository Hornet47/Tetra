from openai import OpenAI
from typing import List

def upload_files(client: OpenAI, file_names: List[str]):
    file_ids = []

    for file_name in file_names:
        print(f"Uploading {file_name}...")

        file = client.files.create(
            file=open(f"files/{file_name}", "rb"), purpose="assistants"
        )
        client.files.wait_for_processing(file.id)
        file_ids.append(file.id)
    return file_ids

def substring(input_string: str, start_substring: str, end_substring: str) -> str:
    start_index = input_string.find(start_substring)
    end_index = input_string.find(end_substring, start_index + len(start_substring))

    if start_index != -1 and end_index != -1:
        return input_string[start_index + len(start_substring):end_index]
    else:
        return None
    
def extract_code(input: str) -> [str, str]:
    print("Extracting code...")
    snippet = substring(input, "```python", "```")
    file_name = substring(snippet, "# ", ".py") + ".py"
    start_index = input.find(".py")
    
    if start_index != -1:
        return file_name, snippet
    else:
        return None
    
def extract_sql(input: str) -> str:
    print("Extracting sql...")
    snippet = substring(input, "```sql", "```")
    return snippet