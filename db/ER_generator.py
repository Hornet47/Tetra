import psycopg2
import json

config_file_path = 'db_config.json'

with open(config_file_path, 'r') as file:
    config = json.load(file)

# Define the connection parameters
dbname = config["dbname"]
user = config["user"]
password = config["password"]
host = config["host"]

def get_table_definitions():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = conn.cursor()

    # Query to get table definitions, including foreign keys
    query = """
    SELECT
        cl.relname AS "table",
        att.attname AS "column",
        pg_catalog.format_type(att.atttypid, att.atttypmod) AS "datatype",
        (SELECT
            cl2.relname AS "foreign_table"
         FROM
            pg_catalog.pg_class cl2
            JOIN pg_catalog.pg_constraint con ON con.confrelid = cl2.oid
         WHERE
            con.conrelid = cl.oid AND att.attnum = ANY(con.conkey)
         LIMIT 1) AS "foreign_table"
    FROM
        pg_catalog.pg_class cl
        JOIN pg_catalog.pg_namespace ns ON ns.oid = cl.relnamespace
        JOIN pg_catalog.pg_attribute att ON att.attrelid = cl.oid AND att.attnum > 0
    WHERE
        cl.relkind = 'r'
        AND ns.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema')
        AND NOT att.attisdropped
    ORDER BY
        cl.relname, att.attnum;
    """

    # Execute the query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Process the rows into a JSON structure
    tables_def = {}
    for row in rows:
        table, column, datatype, foreign_table = row
        if table not in tables_def:
            tables_def[table] = {'columns': [], 'foreign_keys': {}}
        column_def = {'column_name': column, 'data_type': datatype}
        tables_def[table]['columns'].append(column_def)
        if foreign_table:
            tables_def[table]['foreign_keys'][column] = foreign_table

    return tables_def

# Get the table definitions
table_definitions = get_table_definitions()

with open('ER.json', 'w') as outfile:
    json.dump(table_definitions, outfile, indent=2)
