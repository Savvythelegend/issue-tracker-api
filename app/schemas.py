from pydantic import BaseModel, EmailStr, constr


# --- Issue Schemas ---
class IssueCreate(BaseModel):
    title: str
    description: str


class IssueOut(IssueCreate):
    id: int

    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2


# --- User Schemas ---
class UserIn(BaseModel):
    email: EmailStr
    password: constr(min_length=6)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2
