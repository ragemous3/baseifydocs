
defaultPrompt: str =  "You are a technical writer whose role is to make text more readable. You're provided with chunks in html. Make the text better and return the text you improved wrapped in html. Do not return any content wrapped in markdown e.g. no '```html.'"

sysPrompt: dict[str] = {
	"role": "system",
	"content": defaultPrompt
}	

sysPromptMemory: dict[str] = {
	"role": "system",
	"content": f"{defaultPrompt} For every chunk you get you respond with 'chunk <chunk_number>' until I reply with 'chunk <chunk_number>', then you return me that chunk i request"
}	

def get_messages(prompt_type: str) -> list[dict]:
	if prompt_type == "memory":
		return [sysPromptMemory]
	return  sysPrompt