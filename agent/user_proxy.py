import subprocess
from db.dbcontext import Dbcontext

def write_into_file(file_name: str, file_content: str):
    print("Writing into file...")
    with open(f"files/{file_name}", 'w') as file:
        file.write(file_content)
        
def execute(file_name: str):
    print("Executing file...")
    try:
        result = subprocess.run(['python', f"files/{file_name}"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
    
def run_sql(query: str):
    with Dbcontext() as pg:
        pg.connect()
        res = pg.run_sql(query)
    return res

def ask(agent_name:str, query: str):
    return