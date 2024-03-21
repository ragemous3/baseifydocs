from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def make_better(html: str):
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  messages=[
    {"role": "system", "content": "You are a techniqal writer whose role is to make provided text more readable, also to add more or better examples and explain terms to non technical persons. ."},
    {"role": "user", "content": html}
  ])
  return completion.choices[0].message.content
    

