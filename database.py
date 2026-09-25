import psycopg2
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Connect to PostgreSQL
connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = connection.cursor()

# Business query
query = """
SELECT product, SUM(revenue) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;
"""

cursor.execute(query)

results = cursor.fetchall()

print("Total Revenue by Product:")
print("-------------------------")

for product, revenue in results:
    print(f"{product}: ₹{revenue}")

cursor.close()
connection.close()