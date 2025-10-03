# app/db/base.py
from sqlalchemy.orm import declarative_base

# Single Base for all models to share metadata & create tables easily
Base = declarative_base()
