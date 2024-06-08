import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def GPT(
	prompt: list[dict],
):
	completion = client.chat.completions.create(
		model="gpt-3.5-turbo", messages=prompt
	)
	return completion
