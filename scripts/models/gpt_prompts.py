GPT_EOF = "All good"
defaultPrompt: str =  "You are a technical writer whose role is to make text more readable. You're provided with chunks in html. Make the text better. Return the text placed in the same html as you got it. "
addStyles: str = "Also include a great style sheet. Add a Banner with WebGL animation."
tableOfContent: str = "Add a table of contet"
errorHandling: str = f"Return '{GPT_EOF}' if you think no improvements can be made."

sysPrompt: dict[str] = {
	"role": "system",
	"content": defaultPrompt
}	

sysPromptMemory: dict[str] = {
	"role": "system",
	"content": f"You are a technical writer whose role is to make text better. \
 For every chunk you get you respond with 'chunk <chunk_number>' until I reply with 'chunk <chunk_number>', then you return me that chunk i requested with the improvements you've made. \
 NOTE: Return all the html as you got it except if told otherwise. Do not return any content wrapped in markdown. {errorHandling}"
}	

sysPromptMemoryWhole: dict[str] = {
	"role": "system",
	"content": f"You are given chunks of HTML in multiple parts. Your job is to:
1. Preserve the HTML structure and tags.
2. Fix or reformat the text content inside the tags without modifying the HTML structure.
3. Concatinate the fixed chunks and return them in whole.
The HTML will be sent to you in parts. Please wait until I send the last part before returning the complete fixed HTML. I will indicate the final part with the message: 'END OF HTML'.
For each chunk, just acknowledge that you’ve received it and are holding it for processing.
. {errorHandling}"
}	

sysPromptWhole: dict[str] = {
	"role": "system",
	"content": f"You are a technical writer whose role is to make text better. \
	Improve the given html document your given. Remove text if unecessary \
 	NOTE: Return all the html as you got it except if told otherwise. Do not return any content wrapped in markdown. \
 	 {errorHandling}"
}	



def get_messages(prompt_type: str) -> list[dict]:
	if prompt_type == "memory":
		return [sysPromptMemory]
	if prompt_type == "whole":
		return [sysPromptWhole]
	return [sysPrompt]