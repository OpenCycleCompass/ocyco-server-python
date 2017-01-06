from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(session_options=dict(expire_on_commit=False))
