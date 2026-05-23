from services.api import ApiClient


class ResumeApi:

    @staticmethod
    def upload_resume(
        file,
        jd
    ):

        return ApiClient.post(
            "/resumes/upload",
            files={
                "file": (
                    file.name,
                    file,
                    file.type
                )
            },
            data={
                "job_description": jd
            }
        )