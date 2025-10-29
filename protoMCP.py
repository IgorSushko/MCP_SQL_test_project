import os
from mcp.server.fastmcp import FastMCP
import psycopg2

mcp = FastMCP(name="Igor's_first_MCP", 
              instructions="Created for testing purpose, to check MCP SQL")

def load_properties():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'db_config.properties')
    props = {}
    with open(config_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            props[key.strip()] = value.strip()
    return props

@mcp.tool()
def get_sales_persons():
    props = load_properties()

    try:
        connection = psycopg2.connect(
            host=props.get('host'),
            port=props.get('port'),
            database=props.get('database'),
            user=props.get('user'),
            password=props.get('password')
        )

        cursor = connection.cursor()
        cursor.execute("select * from sales.employee order by id desc;")
        salesList = cursor.fetchall()
    except Exception as e:
        return None, None

    return salesList    


if __name__ == "__main__":
    mcp.run()
