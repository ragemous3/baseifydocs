import os
import json
from typing import Generator

from openai import OpenAI
from models.gpt_prompts import *
import nltk
from data.gpt import GPT

# Make startpoint
def main_endpoint(html: str, memory=False):
	if memory:
		return send_memorised(chunk_generator(html))
	else:
		return send_chunks(chunk_generator(html))
		
def chunk_generator(text, chunk_size=500) -> Generator[str, None, None]:
	sentences = nltk.sent_tokenize(text)
	current_tokens = 0
	current_batch = []

	for sentence in sentences:
		# Tokenize the sentence into words
		word_tokens = nltk.word_tokenize(sentence)
		sentence_length = len(word_tokens)
		
		# Check if adding this sentence would exceed the max_tokens limit
		if current_tokens + sentence_length > chunk_size:
			# Yield the current batch as a single string
			yield ' '.join(current_batch)
			# Reset for the next batch
			current_tokens = sentence_length
			current_batch = [sentence]
		else:
			current_tokens += sentence_length
			current_batch.append(sentence)
	
	# Yield any remaining sentences in the last batch
	if current_batch:
		yield ' '.join(current_batch)

	
# Make instruction to have AI give back chunks
def send_chunks(chunk_gen):
	chunk_count = 0
	document = ''
	try:
		while True:
			c = next(chunk_gen)
			chunk_count += 1
			completion = GPT([*get_messages(), {"role": "user", "content": c}])
			document += completion.choices[0].message.content
	except StopIteration:
		print("Generator exhausted. No more values to yield.")  
	return document

def input_chunks(chunk_gen: Generator[str, None, None], messages: list[dict]) -> list[dict]:
	chunk_count = 0
	try:
		while True:
			c = next(chunk_gen)
			chunk_count += 1
			messages = [*messages, {"role": "user", "content": c}]
			completion = GPT(messages)
			messages.append(completion.choices[0].message)
	except StopIteration:
		print("Generator exhausted. No more values to yield.")
		return messages, chunk_count

def output_chunks(messages: list[dict], chunk_count: int):
	document = ''
 
	for chunk_num in range(chunk_count):
		messages = [*messages, {"role": "user", "content": f'chunk {chunk_num + 1}'}]
		text = GPT(messages)
		messages.append(text.choices[0].message)
		document += text.choices[0].message.content
	
	return document, messages


def send_memorised(chunk_gen):
	messages, chunk_count = input_chunks(chunk_gen, get_messages("memory"))
	document, logs = output_chunks(messages, chunk_count)
	
	with open("logs.json", "w") as file:
		file.write(json.dumps(str(logs)))
	
	return document

	
