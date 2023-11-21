from datetime import datetime
import json
import psycopg2


class Dbcontext:
    """
    A class to manage postgres connections and queries
    """
    config_file_path = 'db/db_config.json'

    with open(config_file_path, 'r') as file:
        config = json.load(file)

    # Define the connection parameters
    dbname = config["dbname"]
    user = config["user"]
    password = config["password"]
    host = config["host"]

    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def connect(self):
        self.conn = psycopg2.connect(dbname=Dbcontext.dbname, user=Dbcontext.user, password=Dbcontext.password, host=Dbcontext.host)
        self.cur = self.conn.cursor()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def run_sql(self, sql) -> str:
        """
        Run a SQL query against the postgres database
        """
        self.cur.execute(sql)
        columns = [desc[0] for desc in self.cur.description]
        res = self.cur.fetchall()

        list_of_dicts = [dict(zip(columns, row)) for row in res]

        json_result = json.dumps(list_of_dicts, indent=4, default=self.datetime_handler)

        return json_result

    def datetime_handler(self, obj):
        """
        Handle datetime objects when serializing to JSON.
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)  # or just return the object unchanged, or another default value