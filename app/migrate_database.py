from database import Base, engine
from models import Post


Base.metadata.create_all(engine)