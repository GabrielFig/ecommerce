from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.base import BaseModel, MetadataMixin
from datetime import datetime
from passlib.context import CryptContext

class User(BaseModel, MetadataMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

    # Add relationships if needed
    # orders = relationship("Order", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, is_active={self.is_active}, is_superuser={self.is_superuser})>"

    def check_password(self, password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        return pwd_context.verify(password, self.hashed_password)
        pass

    def set_password(self, password: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.hashed_password = pwd_context.hash(password)
        pass
