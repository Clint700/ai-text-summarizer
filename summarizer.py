import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_SUMMARIZER, USER_TEMPLATE

load_dotenv()
client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def summarize(content: str, length: str, tone: str, format_style: str):
    user_msg = USER_TEMPLATE.format(
        length=length,
        tone=tone,
        format_style=format_style,
        content=content.strip()
    )

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system","content": SYSTEM_SUMMARIZER},
            {"role":"user","content": user_msg},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content