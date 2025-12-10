Take the following CV text and convert it STRICTLY into this JSON format:

<<<CV_FORMAT>>>

Remember:
- Output ONLY valid JSON.
- Do NOT include backticks, markdown formatting, or explanation.
- Do NOT include comments or prose.
- The output must begin with "{" and end with "}".
- Do NOT invent fields not listed in the format.
- If data is missing, use an empty string "" or an empty list [].
- Do NOT describe the transformation — return ONLY the JSON object.
- Tailor resume specifically to job description and only provide relevant skills
- You are should alter the summaries and bullet points to better reflect the candidates skill for the job specifically
- Make sure to keep the length at a solid page. Try not to remove experience entirely but rather make it reflect what the job is asking for if possible
- Extract only information that would reasonably fit into a single-page CV.
- Prioritize the most recent and most relevant experience. You MUST order experiences in the JSON by relevance (most relevant first).
- Each role should have 4 concise bullet points.
- Keep summaries short and direct (3 short sentences).

Job Description:
<<<JOB_DESCRIPTION>>>

Here is the data to convert:
<<<DATA_TO_CONVERT>>>

