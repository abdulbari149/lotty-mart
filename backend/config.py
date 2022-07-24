import os 
class Config:
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")