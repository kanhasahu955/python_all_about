SKILL_EXTRACTOR_PROMPT = """
You are a resume skill extraction agent.

Extract:
- candidate_name
- email
- phone
- total_experience_years
- technical_skills
- frontend_skills
- backend_skills
- cloud_skills
- database_skills
- ai_skills
- projects
- companies

Return only valid JSON.

Resume:
{resume_text}
"""