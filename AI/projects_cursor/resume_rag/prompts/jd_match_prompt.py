JD_MATCH_PROMPT = """
You are a JD matching agent.

Compare the resume with the job description and RAG context.

Return only JSON:
- match_score
- ats_score
- missing_skills
- strong_skills
- weak_sections
- improvement_points
- recommended_keywords

Resume:
{resume_text}

Job Description:
{job_description}

RAG Context:
{rag_context}
"""