from typing import TypedDict

class ResumeState(TypedDict):
    resume_path: str
    resume_text: str
    skills: str
    job_description: str
    context: list
    jd_match: str
    optimized_resume: str
    questions: list
    final_score: int