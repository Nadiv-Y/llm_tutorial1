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
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        top_p=0.9,
        max_tokens=100,
    )

    return response.choices[0].message.content


print(get_completion("what is the capital of France?"))
print(get_completion("what is the number of the population there?"))

"""
cat 0.6
dog 0.2
moon 0.05
apple 0.15

"""