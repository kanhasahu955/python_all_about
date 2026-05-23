RESUME_BUILDER_PROMPT = """
You are an expert resume builder.

Rewrite the resume for the target job description.
Use measurable impact, ATS keywords, strong bullet points, and clean markdown.

Resume:
{resume_text}

Job Description:
{job_description}

JD Match:
{jd_match_json}

Return only markdown.
"""