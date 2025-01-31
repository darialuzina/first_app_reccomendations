from sqlalchemy import Column, Integer, String

from database import Base, SessionLocal, engine

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)




if __name__ == "__main__":
    session = SessionLocal()
    results = []
    filtered_data = (
        session.query(Post)
        .filter(Post.topic == "business")
        .order_by(Post.id.desc())
        .limit(10)
        .all()
    )
    for x in filtered_data:
        results.append(x.id)
    print(results)

