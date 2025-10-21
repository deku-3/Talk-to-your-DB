# 🧠 Natural Language SQL Query Tool

A Python-based **AI-powered query assistant** that allows anyone to interact with a **live server database** using plain English.

## ⚙️ How It Works

1. **User input:**  
   The user types a question in plain English — for example, ***“Show total revenue by region this month.”***

2. **Schema extraction:**  
   The tool connects to the **live database** and automatically fetches its **structure, including table names, columns, primary keys, and foreign key relationships**.

3. **AI query generation:**  
   It sends both the **user question and database schema** to an **AI**, which generates an accurate **SQL query** tailored to the connected database.

4. **Query execution:**  
   The generated **SQL query is executed** directly on the **live database server** to retrieve real-time results.

5. **Insight presentation:**  
   The resulting table and an AI-generated natural language **explanation** are displayed instantly, allowing **non-technical** users and **stakeholders** to understand insights effortlessly.


Perfect for teams who want quick insights without writing a single line of SQL.

---

## 🚀 Key Features
- 🔍 **Query live databases in real time** — no preloaded data required  
- 🧠 **AI-powered SQL generation** — converts natural language into executable SQL  
- 💬 **Human-readable answers** — GPT summarizes results for quick understanding  
- 🧩 **Plug-and-play integration** — works with any SQL database (MySQL, PostgreSQL, SQLite, etc.)  
- 📊 **Result visualization** — tabular output and descriptive summaries in a web UI  
- 🔒 **Secure architecture** — database credentials stay on the server  

---

## 🧰 Tech Stack
| Component | Technology |
|------------|-------------|
| **Backend** | Python |
| **AI Engine** | OpenAI API |
| **Database** | Any SQL DB (MySQL, PostgreSQL, SQLite) |
| **Frontend** | HTML + Jinja Templates |
| **Visualization** | pandas, Bootstrap Table |

---

## 🧩 Use Case Examples
- Data analysts who want quick summaries without writing SQL  
- Business users querying production data securely  
- Internal dashboards for ad-hoc analytics  
- Integration with chatbots or internal tools (e.g., Slack / Telegram bots)

---

## 🪄 Vision
> Turning natural language into data insights — making every database conversational.
