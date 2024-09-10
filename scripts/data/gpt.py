import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def GPT(
	prompt: list[dict],
	model: str
):
	completion = client.chat.completions.create(
		model=model, messages=prompt
	)
	return completion
