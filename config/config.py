import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY","supersecretkey_for_campuscash")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://campuscashuser:CampusCash-2025@localhost/campuscash"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"
    SESSION_PERMENENT = False
    SESSION_USE_SIGNER = True