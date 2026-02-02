from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = init_chat_model(
    "gpt-4o-mini", model_provider="openai"
)   

messages = [SystemMessage(content="You are a recruiter"), HumanMessage(content="I want to apply for a job")]

for token in model.stream(messages):
    print(token.content, end="", flush=True)    