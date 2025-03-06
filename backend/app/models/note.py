from app.models.base import Base, TimestampMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Note(Base, TimestampMixin):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    content = Column(String)
    created_by_id = Column(Integer, ForeignKey("user.id"))

    # Relationships
    subject = relationship("Subject", back_populates="notes")
    created_by = relationship("User", back_populates="notes")
    concept_maps = relationship("NoteConceptMap", back_populates="note")
    example_maps = relationship("NoteExampleMap", back_populates="note")


class NoteConceptMap(Base, TimestampMixin):
    __tablename__ = "note_concept_map"

    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("note.id"))
    concept_id = Column(Integer, ForeignKey("concept.id"))

    # Relationships
    note = relationship("Note", back_populates="concept_maps")
    concept = relationship("Concept", back_populates="note_maps")


class NoteExampleMap(Base, TimestampMixin):
    __tablename__ = "note_example_map"

    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("note.id"))
    example_id = Column(Integer, ForeignKey("example.id"))

    # Relationships
    note = relationship("Note", back_populates="example_maps")
    example = relationship("Example", back_populates="note_maps")
