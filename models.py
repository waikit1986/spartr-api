import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.String, unique=True, nullable=False)
    full_name = sa.Column(sa.String)
    apple_sub = sa.Column(sa.String, unique=True, nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False)


class Profile(Base):
    __tablename__ = "profiles"

    id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
    user_name = sa.Column(sa.String, nullable=False)
    age = sa.Column(sa.Integer)
    bio = sa.Column(sa.Text)

    user = relationship("User", back_populates="profile")
