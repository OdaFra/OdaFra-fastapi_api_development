
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from db.connection import Base

class Posts(Base):
    __tablename__= "posts"
    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String,  nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default='TRUE', nullable = True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))