from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from utils import generate_sql_from_nl, generate_answer_from_table
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI client
client = OpenAI(api_key=openai_api_key) 

# Path to your SQLite database
DB_PATH = 'sales.db'  

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/nl-to-sql', methods=['POST'])
def nl_to_sql():
    question = request.form.get('nl_query')
    if not question:
        return 'No query provided', 400

    try:
        # Step 1: Generate SQL from natural language
        sql_query = generate_sql_from_nl(question, client,DB_PATH)

        # Step 2: Query SQLite database
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()

        # Step 3: Generate final answer from the result table
        answer = generate_answer_from_table(question, df, client)

        # Step 4: Show results
        return render_template(
            'results.html',
            table=df.to_html(classes='data', index=False),
            sql=sql_query,
            answer=answer
        )

    except Exception as e:
        return f'Error processing query: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
