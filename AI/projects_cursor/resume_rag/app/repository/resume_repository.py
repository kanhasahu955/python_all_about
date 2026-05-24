from sqlmodel import Session, select

from app.models.resume_model import ResumeAnalysis, ResumeDocument, ResumeStatus


class ResumeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_document(self, document: ResumeDocument) -> ResumeDocument:
        self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return document

    def list_documents(self) -> list[ResumeDocument]:
        return list(
            self.session.exec(
                select(ResumeDocument).order_by(ResumeDocument.created_at.desc())
            )
        )

    def get_by_document_id(self, document_id: str) -> ResumeDocument | None:
        return self.session.exec(
            select(ResumeDocument).where(ResumeDocument.document_id == document_id)
        ).first()

    def get_analysis(self, document_id: str) -> ResumeAnalysis | None:
        return self.session.exec(
            select(ResumeAnalysis).where(ResumeAnalysis.document_id == document_id)
        ).first()

    def update_status(self, document_id: str, status: ResumeStatus):
        doc = self.get_by_document_id(document_id)
        if doc:
            doc.status = status
            self.session.add(doc)
            self.session.commit()

    def update_job_id(self, document_id: str, job_id: str):
        doc = self.get_by_document_id(document_id)
        if doc:
            doc.job_id = job_id
            self.session.add(doc)
            self.session.commit()

    def save_analysis(self, analysis: ResumeAnalysis) -> ResumeAnalysis:
        self.session.add(analysis)
        self.session.commit()
        self.session.refresh(analysis)
        return analysis
