import uuid
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"
    id          = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status      = Column(String, default="queued")
    progress    = Column(Integer, default=0)
    input_path  = Column(String)
    output_path = Column(String)
    error       = Column(String)
    clips       = relationship("Clip", back_populates="job")

class Clip(Base):
    __tablename__ = "clips"
    id        = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id    = Column(String, ForeignKey("jobs.id"))
    path      = Column(String)
    timestamp = Column(Float)
    score     = Column(Float)
    label     = Column(String, nullable=True)
    job       = relationship("Job", back_populates="clips")