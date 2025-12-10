from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.utils.registry import ExampleRegistry, PromptRegistry, get_example, get_prompt
import os
from dotenv import load_dotenv
import re

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

job_description = \
"""
I need someone who knows unity and object detection
"""

def extract_json(s: str) -> str:
    match = re.search(r'\{.*\}', s, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output.")
    return match.group(0)

async def convert_cv_to_json(
    cv_text: str,
    model: str = "gpt-4.1-mini",
) -> str:
    llm = ChatOpenAI(
        model=model,
        temperature=0.0,  # tighter / deterministic
        api_key=OPENAI_API_KEY,
        model_kwargs={
            "response_format": {"type": "json_object"}
        },
    )
    
    sys_prompt = get_prompt(PromptRegistry.SYSTEM)
    cv_to_json_prompt = get_prompt(PromptRegistry.CV_TO_JSON)
    cv_to_json_example = get_example(ExampleRegistry.CV_JSON_EXAMPLE)
    job_desc = job_description.strip()
    
    system_msg = SystemMessage(content=sys_prompt)
    human_msg = HumanMessage(
        content=cv_to_json_prompt.replace(
            "<<<DATA_TO_CONVERT>>>", cv_text
        ).replace(
            "<<<CV_FORMAT>>>", cv_to_json_example
        ).replace(
            "<<<JOB_DESCRIPTION>>>", job_desc
        )
    )

    resp = await llm.ainvoke([system_msg, human_msg])
    result = resp.content  # should already be pure JSON

    try:
        result = extract_json(result)
    except ValueError as e:
        raise ValueError(f"Failed to extract JSON from the model output. {e}")

    return result

if __name__ == "__main__":
    import asyncio

    with open("fake_cv.txt", "r", encoding="utf-8") as f:
        sample_cv = f.read()

    asyncio.run(convert_cv_to_json(sample_cv))