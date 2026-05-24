import json

import requests

from config import API_BASE_URL
from services.api import ApiClient

WS_BASE_URL = API_BASE_URL.replace("/api/v1", "")


class StreamApi:
    @staticmethod
    def stream_dashboard():
        url = f"{API_BASE_URL}/stream/dashboard"
        with requests.get(url, stream=True, timeout=3600) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                payload = line[6:].strip()
                if not payload:
                    continue
                try:
                    event = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                yield event

    @staticmethod
    def dashboard_websocket_url() -> str:
        host = WS_BASE_URL.replace("http://", "ws://").replace("https://", "wss://")
        return f"{host}/ws/resume"

    @staticmethod
    def stream_analysis(document_id: str):
        url = f"{API_BASE_URL}/stream/analysis/{document_id}"
        with requests.get(url, stream=True, timeout=600) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                payload = line[6:].strip()
                if not payload:
                    continue
                try:
                    event = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                if event.get("event") == "ping":
                    continue
                yield event

    @staticmethod
    def stream_build(resume_text, job_description="", document_id=None):
        url = f"{API_BASE_URL}/stream/build"
        payload = {
            "resume_text": resume_text,
            "job_description": job_description,
        }
        if document_id:
            payload["document_id"] = document_id
        with requests.post(url, json=payload, stream=True, timeout=600) as response:
            if not response.ok:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                raise RuntimeError(detail)
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                yield line[6:]

    @staticmethod
    def stream_llm(prompt: str):
        url = f"{API_BASE_URL}/stream/llm"
        with requests.post(url, json={"prompt": prompt}, stream=True, timeout=120) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                yield line[6:]

    @staticmethod
    def start_interview(skills="", document_id=None):
        payload = {"skills": skills}
        if document_id:
            payload["document_id"] = document_id
        return ApiClient.post("/stream/interview/start", json=payload)

    @staticmethod
    def stream_interview(session_id: str):
        url = f"{API_BASE_URL}/stream/interview/{session_id}"
        with requests.get(url, stream=True, timeout=600) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                payload = line[6:].strip()
                if not payload:
                    continue
                try:
                    event = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                if event.get("event") == "ping":
                    continue
                yield event

    @staticmethod
    def interview_websocket_url(session_id: str) -> str:
        host = WS_BASE_URL.replace("http://", "ws://").replace("https://", "wss://")
        return f"{host}/ws/interview/{session_id}"

    @staticmethod
    def websocket_url(document_id: str) -> str:
        host = WS_BASE_URL.replace("http://", "ws://").replace("https://", "wss://")
        return f"{host}/ws/analysis/{document_id}"
