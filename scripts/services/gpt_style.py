
from data.gpt import GPT
from models.gpt_prompts import sysPromptDefaultStyle


def document_style(prompt: str = sysPromptDefaultStyle, model: str = ""):
    return GPT(prompt, model)