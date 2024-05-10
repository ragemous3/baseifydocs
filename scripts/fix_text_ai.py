from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# test page: https://www.php.net/manual/en/tutorial.firstpage.php

# https://community.openai.com/t/gpt-3-5-turbo-how-to-remember-previous-messages-like-chat-gpt-website/170370/6
def make_better(html: str):
    messages: list[dict] = [
        {
            "role": "system",
            "content": "You are a technical writer whose role is to make text more readable and explain technical terms in a simple way. Your provided with text in html, make that text better. Do not add, modify or remove any html elements, ignore them.",
        },
        {"role": "user", "content": html}
    ]
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125", messages=messages
    )
    
    return completion.choices[0].message.content
