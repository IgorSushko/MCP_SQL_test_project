import os
from mcp.server.fastmcp import FastMCP
import psycopg2

mcp = FastMCP(name="SQL_first_MCP", 
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

def read_props(connectionProps):
    return psycopg2.connect(
            host=connectionProps.get('host'),
            port=connectionProps.get('port'),
            database=connectionProps.get('database'),
            user=connectionProps.get('user'),
            password=connectionProps.get('password')
        )

@mcp.tool()
def get_sales_persons():
    props = load_properties()

    try:
        connection = read_props(props)
        cursor = connection.cursor()
        cursor.execute("select * from sales.employee order by id desc;")
        salesList = cursor.fetchall()
    except Exception as e:
        return None, None

    return salesList    

@mcp.tool()
def get_products():
    props = load_properties()

    try:
        connection = read_props(props)
        cursor = connection.cursor()
        cursor.execute("select * from sales.product order by id desc;")
        productsList = cursor.fetchall()
    except Exception as e:
        return None, None

    return productsList  

@mcp.tool()
def insert_product(sales_id: int, product_name: str, product_quantity: int, product_price: int):
    props = load_properties()
    conn = read_props(props)
    cur = conn.cursor()

    query = "INSERT INTO sales.product (employee_id, name, count, price) VALUES (%s, %s, %s, %s) RETURNING id ;"
    cur.execute(query, (sales_id, product_name,product_quantity,product_price))

    new_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ok", "id": new_id}


if __name__ == "__main__":
    mcp.run()
