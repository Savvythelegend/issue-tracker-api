from pydantic import BaseModel, EmailStr, constr

# --- Issue Schemas ---

class IssueCreate(BaseModel):
    title: str
    description: str

class IssueOut(IssueCreate):  # inherits title & description
    id: int

    class Config:
        orm_mode = True  # allows using .from_orm(model_instance)


# --- User Schemas ---

class UserIn(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
