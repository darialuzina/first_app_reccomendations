from sqlalchemy import Column, Integer, String, func

from database import Base, SessionLocal, engine

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)


if __name__ == "__main__":
    session = SessionLocal()
    results = []
    filtered_data = (
        session.query(User.country, User.os, func.count(User.id))
        .filter(User.exp_group == 3)
        .group_by(User.country, User.os)
        .having(func.count(User.id) > 100)
        .order_by(func.count(User.id).desc())
        .all()
    )
    for x in filtered_data:
        results.append(x)
    print(results)