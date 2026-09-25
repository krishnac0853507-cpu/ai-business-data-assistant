# AI Business Data Assistant

An AI-powered business data assistant that allows users to ask business questions in natural language and receive answers from a PostgreSQL database.

The application uses Gemini to convert natural-language questions into SQL queries, executes those queries on PostgreSQL, and then converts the database results into clear business-friendly answers.

## 🚀 Features

- Ask business questions using natural language
- Automatically generate PostgreSQL queries using Gemini
- Execute queries on a PostgreSQL sales database
- Restrict AI-generated queries to read-only `SELECT` operations
- Convert database results into simple business answers
- FastAPI backend for API communication
- Simple web-based frontend
- Indian Rupee (₹) formatting for monetary results

## 🛠️ Tech Stack

- **Python**
- **PostgreSQL**
- **Gemini API**
- **FastAPI**
- **Psycopg2**
- **HTML / CSS / JavaScript**
- **Git & GitHub**

## 🏗️ How It Works

```text
User Question
      ↓
   Gemini AI
      ↓
SQL Query Generation
      ↓
PostgreSQL Database
      ↓
Database Result
      ↓
   Gemini AI
      ↓
Business-Friendly Answer
      ↓
     User