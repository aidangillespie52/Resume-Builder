# app/utils/latex.py

from pathlib import Path
import re

def latex_escape(text: str) -> str:
    if not isinstance(text, str):
        return text

    # Escape &, %, $, #, _, ~, ^
    # but ONLY when they are NOT already escaped with a backslash.
    text = re.sub(r'(?<!\\)&', r'\&', text)
    text = re.sub(r'(?<!\\)%', r'\%', text)
    text = re.sub(r'(?<!\\)\$', r'\$', text)
    text = re.sub(r'(?<!\\)#', r'\#', text)
    text = re.sub(r'(?<!\\)_', r'\_', text)
    text = re.sub(r'(?<!\\)~', r'\textasciitilde{}', text)
    text = re.sub(r'(?<!\\)\^', r'\textasciicircum{}', text)

    return text

def cleanup_aux_files(tex_path: Path) -> None:
    for ext in [".aux", ".log", ".out", ".toc"]:
        f = tex_path.with_suffix(ext)
        if f.exists():
            f.unlink()
    texput = tex_path.parent / "texput.log"
    if texput.exists():
        texput.unlink()
