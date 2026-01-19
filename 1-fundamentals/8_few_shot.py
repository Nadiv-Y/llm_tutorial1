#clarity
#specificity
#context
#constraints


from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def get_completion(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a translator that got a text and translate it to slang"},
            {"role": "user", "content": f"""
                Translate the delimited text into slang:
                
                '''{prompt}'''

                but first assume you got from the user  the delimited text:
                                
                '''Hello, how are you?'''
                
                in this case you should answer the delimited text:
                
                '''hey, wassup?'''
                
                another example:
                
                you got from the user  the delimited text:


                '''I enjoy eating pizza.'''
                
                 in this case you should answer the delimited text:
                
                I dig pizza!
            """}
        ]
    )

    return response.choices[0].message.content


prompt = "how are you?"
print(get_completion(prompt))