from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv()

model = init_chat_model(
    "gpt-4o-mini", model_provider="openai"
)   

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from english to {language}"),
    ("user", "{text}"),
])

prompt = prompt_template.invoke({"language": "french", "text": "Hello, how are you?"})

response = model.invoke(prompt)

print(response.content)
