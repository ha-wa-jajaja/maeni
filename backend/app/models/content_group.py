from app.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ContentGroup(Base, TimestampMixin):
    __tablename__ = "content_group"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="content_groups")
    subject = relationship("Subject", back_populates="content_groups")
    concept_maps = relationship(
        "ContentGroupConceptMap", back_populates="content_group"
    )
    example_maps = relationship(
        "ContentGroupExampleMap", back_populates="content_group"
    )


class ContentGroupConceptMap(Base, TimestampMixin):
    __tablename__ = "content_group_concept_map"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("content_group.id"))
    concept_id = Column(Integer, ForeignKey("concept.id"))
    rank = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    content_group = relationship("ContentGroup", back_populates="concept_maps")
    concept = relationship("Concept", back_populates="content_group_maps")


class ContentGroupExampleMap(Base, TimestampMixin):
    __tablename__ = "content_group_example_map"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("content_group.id"))
    example_id = Column(Integer, ForeignKey("example.id"))
    rank = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    content_group = relationship("ContentGroup", back_populates="example_maps")
    example = relationship("Example", back_populates="content_group_maps")
