from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.utils.registry import PromptRegistry
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_json(text: str) -> str:
    """
    Extract JSON substring from text.
    Assumes the first '{' and the last '}' enclose the JSON.
    """
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in the text.")
    return text[start:end]

async def convert_cv_to_json(cv_text: str, model: str = "gpt-4.1-mini") -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", PromptRegistry.SYSTEM.value),
        ("human", "Convert the following CV text to JSON format:\n\n{cv_text}")
    ])

    model = ChatOpenAI(
        model=model,
        temperature=0.2,
        api_key=OPENAI_API_KEY
    )

    parser = StrOutputParser()

    chain = prompt | model | parser

    result = chain.invoke({"cv_text": cv_text})
    
    try:
        result = extract_json(result)
    except ValueError:
        raise ValueError("Failed to extract JSON from the model output.")
    
    print(result)
    return result

if __name__ == "__main__":
    import asyncio

    with open("fake_cv.txt", "r", encoding="utf-8") as f:
        sample_cv = f.read()

    asyncio.run(convert_cv_to_json(sample_cv))