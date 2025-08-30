# LangChain Chat with SQL — Natural‑Language to SQL for SQLite & MySQL

Turn plain English into SQL queries and get live results — with conversation memory and a one‑click **Clear history**. Built with **LangChain**, works with **SQLite** or **MySQL**, and supports **OpenAI** or **Groq** as the LLM backend.

---

## Highlights

* 💬 **Ask in English → SQL**: "Top 10 customers by 2024 revenue" → generated SQL + results.
* 🗄️ **Dual DB support**: **SQLite** (zero‑setup) and **MySQL** (production‑ready).
* 🧠 **Conversation memory**: follow‑ups keep context (e.g., "only Q2"), and you can **clear** it anytime.
* 🧩 **LangChain SQL agent**: inspects schema, drafts safe queries, executes, and explains.
* ⚡ **LLMs**: swap between **OpenAI** and **Groq** via env vars.

Link:
---

## Quick Start

### 1) Install

```bash
git clone https://github.com/Vatsal-Founder/LangChainChat-with-SQL-DB.git
cd LangChainChat-with-SQL-DB
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # create if missing
```

### 2) Configure `.env`

Pick an LLM and a database. Use a single `DATABASE_URL` for simplicity.

```ini
# LLM backend
LLM_BACKEND=openai              # openai | groq
OPENAI_API_KEY=your_openai_key  # if openai
# GROQ_API_KEY=your_groq_key    # if groq
MODEL_NAME=gpt-4o-mini          # or llama-3.1-8b (Groq)

# Database (choose one)
# SQLite (local file):

# MYSQL WORKBENCH
# MySQL (MySQL driver):
# MySQL Host=Provide MySQL Host
# MYSQL User=your MYSQL User
# MYSQL password=yourMYSQL password
# MySQL database= yout MySQL database


```

### 3) Run

**Streamlit UI** (default)

```bash
streamlit run sqlapp.py
```

Open [http://localhost:8501](http://localhost:8501)



---

## How to Use

1. **Connect** to a database:

   * SQLite: ensure the file exists (e.g., `./data/APP.db`).
   * MySQL: paste your `MySQL` connection from your local MYSQL Workbench
2. **Ask a question** in plain English.
3. **Follow up** naturally — memory keeps context across turns.
4. Click **Clear history** to start fresh.

### Example prompts

* "List the top 10 products by revenue in 2024."
* "Group by month and show average order value."
* "Filter those results to EMEA and sort descending."
* "Show the SQL you executed." (if your UI supports revealing SQL)

---

## Architecture

```
[UI]
  ↓
[LangChain SQL Agent]
  ├─ Schema inspection (dialect‑aware)
  ├─ NL → SQL (LLM)
  ├─ Execute (SQLite/MySQL)
  └─ Summarize → table + explanation
  ↓
[Conversation memory (clearable)]
```

---

## Notes & Tips

* **Install**: Need to install My SQL Workbench and connect to your database.
* **Safety**: keep the agent read‑only for demos (avoid INSERT/UPDATE/DELETE/DROP).
* **Schema hints**: brief column/table descriptions in prompts improve accuracy.
* **Limits**: cap returned rows and set timeouts to keep responses snappy.

---
