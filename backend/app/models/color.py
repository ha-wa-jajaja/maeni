from app.models.base import Base, TimestampMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Color(Base, TimestampMixin):
    __tablename__ = "color"

    id = Column(Integer, primary_key=True)
    bg = Column(String)
    border = Column(String)
    text = Column(String)

    # Relationships
    concept_types = relationship("ConceptType", back_populates="color")
    tags = relationship("Tag", back_populates="color")


class GradientColor(Base, TimestampMixin):
    __tablename__ = "gradient_color"

    id = Column(Integer, primary_key=True)
    from_color = Column(
        "from", String
    )  # 'from' is a Python keyword, so we need to use a different name
    to = Column(String)
    border = Column(String)

    # Relationships
    subjects = relationship("Subject", back_populates="gradient_color")
