import os
import logging
from typing import List, Tuple, Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="SQL_first_MCP", 
              instructions="Created for testing purpose, to check MCP SQL")

def load_properties() -> Dict[str, str]:
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

def read_props(connectionProps:Dict[str, str]) -> psycopg2.extensions.connection:
    return psycopg2.connect(
            host=connectionProps.get('host'),
            port=connectionProps.get('port'),
            database=connectionProps.get('database'),
            user=connectionProps.get('user'),
            password=connectionProps.get('password')
        )

@mcp.tool()
def get_sales_persons() -> Optional[List[Tuple]]:
    props = load_properties()

    try:
        with read_props(props) as connection:
            with connection.cursor() as cursor:
                cursor.execute("select * from sales.employee order by id desc;")
                salesList = cursor.fetchall()
        return salesList
    except Exception as e:
        logger.error(f"Error fetching sales persons: {e}")
        return None  

@mcp.tool()
def get_products()-> Optional[List[Tuple]]:
    props = load_properties()

    try:
        with read_props(props) as connection:
            with connection.cursor() as cursor:
                cursor.execute("select * from sales.product order by id desc;")
                productsList = cursor.fetchall()
        return productsList
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return None  

@mcp.tool()
def insert_product(sales_id: int, product_name: str, product_quantity: int, product_price: int) -> Dict[str, Any]:
    props = load_properties()
    conn = read_props(props)
    try:
        with read_props(props) as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO sales.product (employee_id, name, count, price) VALUES (%s, %s, %s, %s) RETURNING id;"
                cur.execute(query, (sales_id, product_name, product_quantity, product_price))
                new_id = cur.fetchone()[0]
                conn.commit()
                return {"status": "ok", "id": new_id}
    except Exception as e:
        logger.error(f"Error inserting product: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    mcp.run()