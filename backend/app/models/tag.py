from app.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Tag(Base, TimestampMixin):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    color_id = Column(Integer, ForeignKey("color.id"))
    name = Column(String, nullable=False)
    public = Column(Boolean, default=False)
    created_by_id = Column(Integer, ForeignKey("user.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    color = relationship("Color", back_populates="tags")
    created_by = relationship("User", back_populates="tags")
    item_tags = relationship("ItemTagMap", back_populates="tag")
    example_tags = relationship("ExampleTagMap", back_populates="tag")


class ItemTagMap(Base, TimestampMixin):
    __tablename__ = "item_tag_map"

    id = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey("concept.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    concept = relationship("Concept", back_populates="item_tags")
    tag = relationship("Tag", back_populates="item_tags")


class ExampleTagMap(Base, TimestampMixin):
    __tablename__ = "example_tag_map"

    id = Column(Integer, primary_key=True)
    example_id = Column(Integer, ForeignKey("example.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    example = relationship("Example", back_populates="example_tags")
    tag = relationship("Tag", back_populates="example_tags")
