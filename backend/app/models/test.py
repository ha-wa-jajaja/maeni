from app.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class TestType(Base, TimestampMixin):
    __tablename__ = "test_type"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # 'strict' or 'loose'
    is_deleted = Column(Boolean, default=False)

    # Relationships
    tests = relationship("Test", back_populates="type")


class Test(Base, TimestampMixin):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey("test_type.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    created_by_id = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    type = relationship("TestType", back_populates="tests")
    subject = relationship("Subject", back_populates="tests")
    created_by = relationship("User", back_populates="tests")
