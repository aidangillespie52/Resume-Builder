from pathlib import Path
import json
import subprocess
import shutil
import os

# main.py is inside src/, so we use relative import
from src.render import render_education, render_experience, render_projects, render_skills
from src.utils import cleanup_aux_files

# Paths
ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "layouts" / "bajaj.tex"
DATA_PATH     = ROOT / "data.json"
OUTPUT_TEX    = ROOT / "resume.tex"
OUTPUT_DIR    = ROOT / "output"


def run_pdflatex(tex_path: Path):
    """
    Run pdflatex on the given .tex file and move the PDF into OUTPUT_DIR.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Run pdflatex in the directory where the .tex file lives (project root)
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_path.name],
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
    )

    pdf = tex_path.with_suffix(".pdf")

    if not pdf.exists():
        # Real failure: show LaTeX output so you can debug
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("⚠ LaTeX compile failed — resume.pdf not created")

    # Move pdf into output/
    final_path = OUTPUT_DIR / pdf.name
    shutil.move(str(pdf), final_path)

    if result.returncode != 0:
        print("pdflatex returned non-zero, but PDF was generated.")

    print(f"✔ PDF saved → {final_path}")
    cleanup_aux_files(tex_path)
    
    return final_path

def main():
    # Read template + data
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    data = json.load(DATA_PATH.open("r", encoding="utf-8"))

    # Render sections
    education_block = render_education(data["education"])
    experience_block = render_experience(data["experience"])
    projects_block = render_projects(data["projects"])
    skills_block = render_skills(data["skills"])

    # Fill placeholders
    filled = (
        template
        .replace("<<NAME>>", data["name"])
        .replace("<<EMAIL>>", data["email"])
        .replace("<<PHONE>>", data["phone"])
        .replace("<<LINKEDIN_URL>>", data["linkedin"])
        .replace("<<EDUCATION_BLOCK>>", education_block)
        .replace("<<EXPERIENCE_BLOCK>>", experience_block)
        .replace("<<PROJECTS_BLOCK>>", projects_block)
        .replace("<<SKILLS_BLOCK>>", skills_block)
    )

    # Write resume.tex at project root
    OUTPUT_TEX.write_text(filled, encoding="utf-8")

    # Compile → output/resume.pdf
    run_pdflatex(OUTPUT_TEX)


if __name__ == "__main__":
    main()
