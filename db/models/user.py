from sqlalchemy import Boolean, Column, Integer, String

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, default=None)
    last_name = Column(String, default=None)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    otp = Column(Integer)
    is_active = Column(Boolean, default=True)

    def hash_password(self):
        from utils.user import get_password_hash
        self.password = get_password_hash(self.password)

