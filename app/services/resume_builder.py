# app/services/resume_builder.py

# imports
import asyncio
from pathlib import Path
import json
import requests
from urllib.parse import quote
import subprocess
import tempfile

# local imports
from app.utils.latex import cleanup_aux_files, latex_escape
from app.renderers.simple import SimpleRenderer
from app.renderers.base import BaseRenderer
from app.utils.registry import get_template, TemplateRegistry
from app.services.ai_client import convert_cv_to_json

OUTPUT_DIR = Path("output")
OUTPUT_TEX = Path("output/resume.tex")
OUTPUT_PDF = Path("output/resume.pdf")

def clamp_experiences(
    experiences: list[dict], 
    max_items: int = 5 ) -> list[dict]:
    
    if len(experiences) <= max_items:
        return experiences
    
    return experiences[:max_items]

def clamp_projects(
    projects: list[dict], 
    max_items: int = 3
    ) -> list[dict]:
    
    if len(projects) <= max_items:
        return projects
    
    return projects[:max_items]

def escape_all(obj):
    if isinstance(obj, str):
        return latex_escape(obj)
    elif isinstance(obj, list):
        return [escape_all(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: escape_all(v) for k, v in obj.items()}
    else:
        return obj
    
def tex_to_pdf(tex_src: str, compiler: str = "pdflatex") -> bytes:
    out_dir = Path("debug/latex")
    out_dir.mkdir(exist_ok=True)

    tex_path = out_dir / "resume.tex"
    pdf_path = out_dir / "resume.pdf"
    
    tex_path.write_text(tex_src, encoding="utf-8")

    cmd = [
        compiler,
        "-interaction=nonstopmode",
        "-halt-on-error",
        tex_path.name,
    ]

    result = subprocess.run(
        cmd,
        cwd=out_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print("=== STDOUT ===")
        print(result.stdout)
        print("=== STDERR ===")
        print(result.stderr)
        raise RuntimeError("LaTeX compile failed; see latex_debug/resume.tex and resume.log")

    if not pdf_path.exists():
        raise RuntimeError("pdflatex ran successfully but no PDF was produced.")

    return pdf_path.read_bytes()

def build_resume(
    renderer: BaseRenderer,
    cv_data: str,
    make_file: bool = True) -> None:

    data = json.loads(cv_data)
    
    # clean data
    data = escape_all(data)
    data["experience"] = clamp_experiences(data["experience"], max_items=3)
    data["projects"] = clamp_projects(data["projects"])
    
    # compile tex
    tex_src = renderer.build(data)
    tex_pdf = tex_to_pdf(tex_src)
    
    # output to .pdf
    if make_file:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if not OUTPUT_PDF.exists():
            OUTPUT_PDF.touch()
            
        with OUTPUT_PDF.open("wb") as f:
            f.write(tex_pdf)
    
    return tex_pdf

async def main():
    cv_path = Path("data.json")
    with open(cv_path, "r", encoding="utf-8") as f:
        cv_text = json.load(f)
    
    rdr = SimpleRenderer()
    json_str = await convert_cv_to_json(str(cv_text))
    
    build_resume(rdr, json_str)
    
if __name__ == "__main__":
    asyncio.run(main())
