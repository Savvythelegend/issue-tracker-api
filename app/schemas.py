from pydantic import BaseModel

class IssueCreate(BaseModel):
    title: str
    description: str

class IssueOut(IssueCreate):
    id: int
