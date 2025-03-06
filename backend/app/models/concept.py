from app.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ConceptType(Base, TimestampMixin):
    __tablename__ = "concept_type"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color_id = Column(Integer, ForeignKey("color.id"))
    created_by_id = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    color = relationship("Color", back_populates="concept_types")
    created_by = relationship("User", back_populates="concept_types")
    concepts = relationship("Concept", back_populates="type")


class Concept(Base, TimestampMixin):
    __tablename__ = "concept"

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("concept_type.id"))
    content = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    description = Column(String)
    detail = Column(String)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    created_by_id = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    type = relationship("ConceptType", back_populates="concepts")
    subject = relationship("Subject", back_populates="concepts")
    created_by = relationship("User", back_populates="concepts")
    example_points = relationship("ExamplePointMap", back_populates="concept")
    item_tags = relationship("ItemTagMap", back_populates="concept")
    content_group_maps = relationship(
        "ContentGroupConceptMap", back_populates="concept"
    )
    note_maps = relationship("NoteConceptMap", back_populates="concept")
