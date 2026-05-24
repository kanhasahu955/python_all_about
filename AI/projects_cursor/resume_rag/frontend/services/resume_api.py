from services.api import ApiClient


class ResumeApi:
    @staticmethod
    def upload_resume(file, jd):
        return ApiClient.post(
            "/resumes/upload",
            files={
                "file": (file.name, file.getvalue(), file.type),
            },
            data={
                "job_description": jd or "",
            },
        )

    @staticmethod
    def list_resumes():
        return ApiClient.get("/resumes/")

    @staticmethod
    def retry_analysis(document_id: str):
        return ApiClient.post(f"/resumes/{document_id}/retry")

    @staticmethod
    def get_resume(document_id):
        return ApiClient.get(f"/resumes/{document_id}")

    @staticmethod
    def build_resume(resume_text, job_description=""):
        return ApiClient.post(
            "/resumes/build",
            json={
                "resume_text": resume_text,
                "job_description": job_description,
            },
        )

    @staticmethod
    def generate_interview(skills="", document_id=None):
        payload = {"skills": skills}
        if document_id:
            payload["document_id"] = document_id
        return ApiClient.post("/resumes/interview", json=payload)
