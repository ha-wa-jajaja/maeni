from app.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Example(Base, TimestampMixin):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    question = Column(String)
    answer = Column(String)
    detail = Column(String)
    created_by_id = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    subject = relationship("Subject", back_populates="examples")
    created_by = relationship("User", back_populates="examples")
    example_points = relationship("ExamplePointMap", back_populates="example")
    example_tags = relationship("ExampleTagMap", back_populates="example")
    content_group_maps = relationship(
        "ContentGroupExampleMap", back_populates="example"
    )
    note_maps = relationship("NoteExampleMap", back_populates="example")


class ExamplePointMap(Base, TimestampMixin):
    __tablename__ = "example_point_map"

    id = Column(Integer, primary_key=True)
    example_id = Column(Integer, ForeignKey("example.id"))
    concept_id = Column(Integer, ForeignKey("concept.id"))
    rank = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    example = relationship("Example", back_populates="example_points")
    concept = relationship("Concept", back_populates="example_points")
