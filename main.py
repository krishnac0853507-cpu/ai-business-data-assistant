from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables
load_dotenv()

# Gemini setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


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


@app.get("/")
def home():
    return {"message": "AI Business Data Assistant is running!"}


@app.post("/ask")
def ask_question(data: Question):

    question = data.question

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

    # Remove markdown formatting
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

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

    # Execute SQL
    cursor.execute(sql_query)

    # Get database result
    results = cursor.fetchall()

    # Generate human-friendly answer
    answer_prompt = f""" 
    You are a helpful business data analyst. 
 
    User's question: 
    {question} 
 
    Database result: 
    {results} 
 
    Give a clear and concise answer to the user's question. 
    Include important numbers when available. 
    For all monetary values, ALWAYS use Indian Rupees (₹), never $ or USD.
    Format Indian currency using the Indian numbering system when appropriate.
    Do not mention SQL, Python, Gemini, or technical implementation details. 
    """
    
    answer_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=answer_prompt
    )

    answer = answer_response.text.strip()

    cursor.close()
    connection.close()

    return {
    "question": question,
    "sql": sql_query,
    "result": results,
    "answer": answer
}