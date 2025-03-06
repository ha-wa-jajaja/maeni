from app.models.base import Base, TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Subject(Base, TimestampMixin):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    gradient_color_id = Column(Integer, ForeignKey("gradient_color.id"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="subjects")
    gradient_color = relationship("GradientColor", back_populates="subjects")
    concepts = relationship("Concept", back_populates="subject")
    examples = relationship("Example", back_populates="subject")
    tests = relationship("Test", back_populates="subject")
    content_groups = relationship("ContentGroup", back_populates="subject")
    notes = relationship("Note", back_populates="subject")
