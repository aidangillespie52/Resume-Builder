# render.py

from app.utils.latex import latex_escape

def render_education(education_list):
    blocks = []
    for edu in education_list:
        degree_line = latex_escape(edu["degree"])
        gpa = edu.get("gpa")
        if gpa:
            degree_line += f" — GPA: {latex_escape(gpa)}"

        block = f"""    \\resumeSubheading
      {{{latex_escape(edu['institution'])}}}{{{latex_escape(edu['dates'])}}}
      {{{degree_line}}}{{{latex_escape(edu['details'])}}}
"""
        blocks.append(block)

    return "\n".join(blocks)

def render_experience(experience_list):
    blocks = []
    for exp in experience_list:
        summary_block = ""
        if exp.get("summary"):
            summary_block = (
                f"      \\resumeItem{{Summary}}{{{latex_escape(exp['summary'])}}}\n"
            )

        bullets = "\n".join(
            f"      \\resumeItem{{}}{{{latex_escape(b)}}}"
            for b in exp.get("bullets", [])
        )

        block = f"""    \\resumeSubheading
      {{{latex_escape(exp['company'])}}}{{{latex_escape(exp['dates'])}}}
      {{{latex_escape(exp['role'])}}}{{}}
      \\resumeItemListStart
{summary_block}{bullets}
      \\resumeItemListEnd

"""
        blocks.append(block)

    return "\n".join(blocks)

def render_projects(projects_list):
    blocks = []
    for proj in projects_list:
        # tech can be list or string
        tech = proj.get("tech")
        if isinstance(tech, list):
            tech_str = ", ".join(tech)
        else:
            tech_str = str(tech) if tech else ""

        # Join bullets into one sentence-like string
        bullets = proj.get("bullets", [])
        bullets_str = "; ".join(bullets) if bullets else ""

        # Build description: summary + bullets + tech
        parts = []
        if proj.get("summary"):
            parts.append(latex_escape(proj["summary"]))
        if bullets_str:
            parts.append(f"Key contributions: {latex_escape(bullets_str)}.")
        if tech_str:
            parts.append(f"Tech: {latex_escape(tech_str)}.")
        description = " ".join(parts)

        block = f"""    \\resumeSubItem{{{proj['name']}}}{{{description}}}
"""
        blocks.append(block)

    return "\n".join(blocks)

def render_skills(skills_list):
    skills_str = ", ".join(latex_escape(skill) for skill in skills_list)
    return f"""    \\item{{
     \\textbf{{Skills}}{{: {skills_str}}}
    }}"""