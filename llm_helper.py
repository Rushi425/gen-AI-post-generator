from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

# initialize groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=2,
    stop=None,
)


if __name__ == "__main__":
    print("helloooooo")
 