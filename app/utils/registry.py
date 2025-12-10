# app/prompts/registry.py

from enum import Enum
from pathlib import Path

PROMPTS_DIR = Path("app/prompts")
EXAMPLES_DIR = Path("app/examples")
TEMPLATES_DIR = Path("app/resume_templates")

class PromptRegistry(Enum):
    SYSTEM = "system.md"
    CV_TO_JSON = "convert_cv_json.md"

class ExampleRegistry(Enum):
    CV_JSON_EXAMPLE = "cv_format.json"

class TemplateRegistry(Enum):
    SIMPLE = "simple.tex"
    
def _load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def _load_prompt(prompt_file: str) -> str:
    return _load_file(PROMPTS_DIR / prompt_file)

def _load_example(example_file: str) -> str:
    return _load_file(EXAMPLES_DIR / example_file)

def _load_template(template_file: str) -> str:
    return _load_file(TEMPLATES_DIR / template_file)

def get_prompt(prompt: PromptRegistry) -> str:
    if prompt is PromptRegistry.CV_TO_JSON:
        template = _load_prompt(prompt.value)
        example_json = get_example(ExampleRegistry.CV_JSON_EXAMPLE)
        return template.replace("<<<CV_FORMAT>>>", example_json)

    # default: raw prompt text
    return _load_prompt(prompt.value)

def get_example(example: ExampleRegistry) -> str:
    return _load_example(example.value)

def get_template(template: TemplateRegistry) -> str:
    return _load_template(template.value)