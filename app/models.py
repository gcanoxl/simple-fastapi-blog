from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, func

from app.db import Base


class User(Base):
    _tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, default=1)

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
    )
