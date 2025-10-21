import sqlite3
def generate_sql_from_nl(nl_query, client,db_path):
    schema = get_full_db_schema(db_path)
    print(schema)
    prompt = f"""
    You are a SQL expert.

    Use the following database schema:
    {schema}
    Write a valid SQL query for the following natural language question:

    {nl_query}

    Only return the raw SQL query. Do NOT add explanations, markdown, or formatting.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def generate_answer_from_table(question, df, client):
    prompt = f"""
    You are a data analyst.

    Given the following user question: "{question}"

    And this table data:
    {df.to_dict(orient='records')}

    Answer the question in clear, natural language.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

import sqlite3

def get_full_db_schema(db_path: str) -> str:
    """
    Dynamically extract the database schema including:
    - Table names
    - Column names and types
    - Primary key constraints
    - Foreign key relationships
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema_info = []

    # Fetch all user tables (ignore SQLite internal ones)
    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()

    for (table_name,) in tables:
        # --- Get column definitions ---
        columns = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        column_lines = []
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            pk_flag = " PRIMARY KEY" if col[5] == 1 else ""
            column_lines.append(f"    {col_name} {col_type}{pk_flag}")

        # --- Get foreign key relationships ---
        fkeys = cursor.execute(f"PRAGMA foreign_key_list({table_name})").fetchall()
        fk_lines = []
        for fk in fkeys:
            # Each fk tuple = (id, seq, table, from, to, on_update, on_delete, match)
            fk_lines.append(f"    FOREIGN KEY ({fk[3]}) REFERENCES {fk[2]}({fk[4]})")

        # --- Combine table schema ---
        table_schema = f"TABLE {table_name} (\n" + ",\n".join(column_lines + fk_lines) + "\n)"
        schema_info.append(table_schema)

    conn.close()
    return "\n\n".join(schema_info)
