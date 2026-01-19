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
        ]
    )

    return response.choices[0].message.content


bad_prompt = "Tell me about coding"
good_prompt = """
I am a beginner in coding and I want to learn Python.
Can you explain the basics of Python in a simple and easy-to-understand way?

"""


# print("Bad Prompt:")
# print(get_completion(bad_prompt))

# print("\nGood Prompt:")
# print(get_completion(good_prompt))


text_to_summarize = """
    I went to a therapy session last week and I told him: I'm a junior lecturer in a university and I'm teaching a course on AI for 
    business students. Yesterday, I gave a lecture on the basics of AI, machine
    learning, and deep learning. Today, I want to give a lecture on the applications
    but i feel very nervous about it. Can you help me create a presentation on the 
    applications of AI in business?
"""

summary_prompt = f"""
Summarize the text delimited by triple quotes into a few words:
'''{text_to_summarize}'''
"""
print(f"\nSummary Prompt:\n{summary_prompt}")
print("\nSummary:")
print(get_completion(summary_prompt))
