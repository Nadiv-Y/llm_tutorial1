from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = init_chat_model(
    "gpt-4o-mini", model_provider="openai"
)   

# response = model.invoke("Hello, how are you?")

# print(response.content)


# response1 = model.invoke([{"role": "system", "content": "You are the king of French Luis 14th"}, {"role": "user", "content": "Hello, how are you?"}])

# print(response1.content)

response2 = model.invoke([SystemMessage(content="You are a french frog"), HumanMessage(content="You are nothing but a frog")])

print(response2.content)