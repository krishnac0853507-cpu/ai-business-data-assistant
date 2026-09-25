from google import genai
from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables
load_dotenv()

# Gemini setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Database schema
database_schema = """
Table: sales

Columns:
order_id
order_date
customer_name
region
product
category
quantity
unit_price
discount_pct
revenue
"""

# Ask the user
question = input("Ask your question: ")

# Generate SQL
sql_prompt = f"""
You are a PostgreSQL SQL expert.

Database structure:

{database_schema}

User question:
{question}

Generate ONLY one PostgreSQL SELECT query needed to answer the question.

Rules:
- Only SELECT queries are allowed.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, or GRANT.
- Do not use multiple SQL statements.
- Do not explain the query.
- Do not use markdown.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=sql_prompt
)

sql_query = response.text.strip()

# Remove markdown formatting if Gemini adds it
sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

print("\nGenerated SQL:")
print(sql_query)

# Safety check
dangerous_keywords = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE"
]

sql_upper = sql_query.upper()

if not sql_upper.startswith("SELECT"):
    raise ValueError("Blocked: Only SELECT queries are allowed.")

for keyword in dangerous_keywords:
    if keyword in sql_upper:
        raise ValueError(f"Blocked: {keyword} operation is not allowed.")

# Prevent multiple SQL statements
if ";" in sql_query[:-1]:
    raise ValueError("Blocked: Multiple SQL statements are not allowed.")

# Connect to PostgreSQL
connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = connection.cursor()

# Execute safe SQL
cursor.execute(sql_query)

# Get result
results = cursor.fetchall()

print("\nRaw Database Result:")
print(results)

# Generate human-friendly answer
answer_prompt = f"""
You are a helpful business data analyst.

User's question:
{question}

Database result:
{results}

Give a clear and concise answer to the user's question.
Include important numbers when available.
Use Indian Rupees (₹) for monetary values.
Do not mention SQL, Python, Gemini, or technical implementation details.
"""

answer_response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=answer_prompt
)

print("\nAI Answer:")
print(answer_response.text)

# Close connection
cursor.close()
connection.close()