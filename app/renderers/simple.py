# app/renderers/simple.py

from typing import List

from app.renderers.base import BaseRenderer
from app.utils.latex import latex_escape
from app.utils.registry import TemplateRegistry, get_template


class SimpleRenderer(BaseRenderer):
    def __init__(self):
        super().__init__()
        self.template = get_template(TemplateRegistry.SIMPLE)

    def _format_education_block(
        self,
        institution: str,
        dates: str,
        degree_line: str,
        details: str,
    ) -> str:
        lines = [
            f"\\textbf{{{institution}}} \\hfill {dates} \\\\",
            f"\\textit{{{degree_line}}}\\\\",
        ]

        if details:
            lines.append(f"{details}\\\\")
        lines.append("\\vspace{6pt}")

        return "\n".join(lines) + "\n"

    def _format_experience_block(
        self,
        company: str,
        dates: str,
        role: str,
        summary: str,  # plain text (already escaped), optional
        bullets: str,  # string of "\\item ..." lines, possibly empty
    ) -> str:
        parts = [
            f"\\textbf{{{company}}} \\hfill {dates} \\\\",
            f"\\textit{{{role}}}\\\\",
        ]

        if summary:
            parts.append(f"{summary}\\\\")  # one summary line

        if bullets.strip():
            parts.append("\\begin{itemize}[leftmargin=*]")
            parts.append(bullets)
            parts.append("\\end{itemize}")

        parts.append("\\vspace{6pt}")

        return "\n".join(parts) + "\n"

    def render_education(self, education_list: List[dict]) -> str:
        blocks = []

        for edu in education_list:
            degree_line = latex_escape(edu["degree"])
            gpa = edu.get("gpa")

            if gpa:
                degree_line += f" — GPA: {latex_escape(gpa)}"

            blocks.append(
                self._format_education_block(
                    institution=latex_escape(edu["institution"]),
                    dates=latex_escape(edu["dates"]),
                    degree_line=degree_line,
                    details=latex_escape(edu.get("details", "")),
                )
            )

        return "\n".join(blocks)

    def render_experience(self, experience_list: List[dict]) -> str:
        blocks = []

        for exp in experience_list:
            summary_text = ""
            if exp.get("summary"):
                summary_text = latex_escape(exp["summary"])

            bullets = "\n".join(
                f"  \\item {latex_escape(b)}"
                for b in exp.get("bullets", [])
            )

            block = self._format_experience_block(
                company=latex_escape(exp["company"]),
                dates=latex_escape(exp["dates"]),
                role=latex_escape(exp["role"]),
                summary=summary_text,
                bullets=bullets,
            )

            blocks.append(block)

        return "\n".join(blocks)

    def render_projects(self, projects_list: List[dict]) -> str:
        blocks = []

        for proj in projects_list:
            tech = proj.get("tech")
            if isinstance(tech, list):
                tech_str = ", ".join(tech)
            else:
                tech_str = str(tech) if tech else ""

            bullets = proj.get("bullets", [])
            bullets_str = "; ".join(bullets) if bullets else ""

            parts = []
            if proj.get("summary"):
                parts.append(latex_escape(proj["summary"]))
            if bullets_str:
                parts.append(f"Key contributions: {latex_escape(bullets_str)}.")
            if tech_str:
                parts.append(f"Tech: {latex_escape(tech_str)}.")

            description = " ".join(parts)

            block_lines = [
                f"\\textbf{{{latex_escape(proj['name'])}}}\\\\",
            ]
            if description:
                block_lines.append(f"{description}\\\\")
            block_lines.append("\\vspace{4pt}")

            blocks.append("\n".join(block_lines))

        return "\n".join(blocks)

    def render_skills(self, skills_list: List[str]) -> str:
        return ", ".join(latex_escape(skill) for skill in skills_list)

    def build(self, data: dict) -> str:
        # Render sections
        education_block = self.render_education(data["education"])
        experience_block = self.render_experience(data["experience"])
        projects_block = self.render_projects(data["projects"])
        skills_block = self.render_skills(data["skills"])

        # Fill placeholders in the simple template
        return (
            self.template.replace("<<NAME>>", data["name"])
            .replace("<<EMAIL>>", data["email"])
            .replace("<<PHONE>>", data["phone"])
            .replace("<<LINKEDIN_URL>>", data["linkedin"])
            .replace("<<EDUCATION_BLOCK>>", education_block)
            .replace("<<EXPERIENCE_BLOCK>>", experience_block)
            .replace("<<PROJECTS_BLOCK>>", projects_block)
            .replace("<<SKILLS_BLOCK>>", skills_block)
        )
