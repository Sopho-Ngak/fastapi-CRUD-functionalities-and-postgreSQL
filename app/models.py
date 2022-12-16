import uuid
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, text, Text
from sqlalchemy.dialects.postgresql import UUID


class Post(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    title = Column(String)
    body = Column(String)
    published = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    def __repr__(self):
        return f"Post(title={self.title}, body={self.body}, published={self.published}, created_at={self.created_at})"
