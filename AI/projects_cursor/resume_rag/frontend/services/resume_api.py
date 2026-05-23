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
    def get_resume(document_id):
        return ApiClient.get(f"/resumes/{document_id}")
