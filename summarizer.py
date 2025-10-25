import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_SUMMARIZER, USER_TEMPLATE

load_dotenv()

# Let SDK read OPENAI_API_KEY/OPENAI_MODEL from env/Streamlit secrets
client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# expose last usage for UI
last_usage: dict | None = None

def summarize(content: str, length: str, tone: str, format_style: str) -> str:
    """
    Calls OpenAI to summarize content. Updates global last_usage with token stats.
    """
    global last_usage

    user_msg = USER_TEMPLATE.format(
        length=length,
        tone=tone,
        format_style=format_style,
        content=content.strip()
    )

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_SUMMARIZER},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.2,
    )

    # capture token usage for UI
    u = getattr(resp, "usage", None)
    if u:
        last_usage = {
            "prompt": u.prompt_tokens,
            "completion": u.completion_tokens,
            "total": u.total_tokens,
        }
    else:
        last_usage = None

    return resp.choices[0].message.content