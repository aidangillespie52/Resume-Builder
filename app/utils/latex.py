# app/utils/latex.py

from pathlib import Path

def latex_escape(s: str) -> str:
    """
    Escape characters that have special meaning in LaTeX.
    Use this on any plain-text coming from JSON.
    """
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s

def cleanup_aux_files(tex_path: Path):
    for ext in [".aux", ".log", ".out", ".toc"]:
        f = tex_path.with_suffix(ext)
        if f.exists():
            f.unlink()
    texput = tex_path.parent / "texput.log"
    if texput.exists():
        texput.unlink()
