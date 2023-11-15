def write_into_file(file_name: str, file_content: str):
    with open(file_name, 'w') as file:
        file.write(file_content)
        
def extract_section(input_string: str, start_substring: str, end_substring: str) -> str:
    start_index = input_string.find(start_substring)
    end_index = input_string.find(end_substring, start_index + len(start_substring))

    if start_index != -1 and end_index != -1:
        return input_string[start_index + len(start_substring):end_index]
    else:
        return None