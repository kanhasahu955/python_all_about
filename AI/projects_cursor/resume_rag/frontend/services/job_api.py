from services.api import ApiClient


class JobApi:
    @staticmethod
    def get_job(job_id):
        return ApiClient.get(f"/jobs/{job_id}")
