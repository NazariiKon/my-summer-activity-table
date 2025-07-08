from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date 
from src.database import Base

class TaskModel(Base):
    __tablename__ = "tblTask"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    completed: Mapped[bool]

    day_id: Mapped[int] = mapped_column(ForeignKey("tblDay.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("tblCategory.id"))

    day: Mapped["DayModel"] = relationship(back_populates="activities")
    category: Mapped["CategoryModel"] = relationship(back_populates="activities")

class DayModel(Base):
    __tablename__ = "tblDay"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    activities: Mapped[list["TaskModel"]] = relationship(back_populates="day")

class CategoryModel(Base):
    __tablename__ = "tblCategory"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    activities: Mapped[list["TaskModel"]] = relationship(back_populates="category")
