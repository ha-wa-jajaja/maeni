from app.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Role(Base, TimestampMixin):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationships
    users = relationship("User", back_populates="role")


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    firebase_uid = Column(String, unique=True, nullable=False)
    display_name = Column(String)
    email = Column(String)
    role_id = Column(Integer, ForeignKey("role.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    role = relationship("Role", back_populates="users")
    subjects = relationship("Subject", back_populates="user")
    concepts = relationship("Concept", back_populates="created_by")
    examples = relationship("Example", back_populates="created_by")
    concept_types = relationship("ConceptType", back_populates="created_by")
    tests = relationship("Test", back_populates="created_by")
    tags = relationship("Tag", back_populates="created_by")
    content_groups = relationship("ContentGroup", back_populates="user")
    notes = relationship("Note", back_populates="created_by")
