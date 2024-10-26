import os
from sqlalchemy import create_engine, text
from llama_index.core.indices.struct_store import GPTSQLStructStoreIndex
from llama_index.core import SQLDatabase

from chainlit import App, UserMessage, BotMessage
from llama_index.llms.openai import OpenAI

# Environment variables
POSTGRES_URL = os.getenv("POSTGRES_URL")  # Example: "postgresql://user:password@localhost:5432/database"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # Set for LlamaIndex

# Initialize database engine
engine = create_engine(POSTGRES_URL)
sql_database = SQLDatabase(engine)

# Initialize LlamaIndex with OpenAI LLM
llm = OpenAI(model="gpt-4o-mini-2024-07-18")
index = GPTSQLStructStoreIndex.from_sql_database(sql_database, llm=llm)

# Initialize Chainlit app
app = App(title="Postgres LlamaIndex Chatbot", description="Interact with PostgreSQL via LlamaIndex agents")


@app.route("/", methods=["POST"])
async def chat(request):
    """
    Main chatbot route using LlamaIndex for SQL generation and execution.
    """
    user_message = request.data.get("content")

    if not user_message:
        return BotMessage("Please enter a message.")

    try:
        # Generate SQL query using LlamaIndex
        response = index.query(user_message, sql_database=sql_database)
        sql_query = response.raw_sql

        # Execute the SQL query
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            rows = result.fetchall()
            column_names = result.keys()
            # Format query results
            formatted_data = [dict(zip(column_names, row)) for row in rows]
            return BotMessage(f"Query Result:\n{formatted_data}")
    except Exception as e:
        return BotMessage(f"Error processing request: {str(e)}")


if __name__ == "__main__":
    # Run Chainlit app
    import chainlit

    chainlit.run(app, host="localhost", port=11111, debug=True)
