# Testing-specific configurations

class Config:
    DATABASE = 'instance/trade_hub_database.sqlite'

class TestConfig(Config):
    # Pfad zur Test-Datenbank
    DATABASE = 'instance/test_trade_hub_database.sqlite'
    # SQLAlchemy URI für SQLite-Datenbank (falls du SQLAlchemy verwendest)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/test_database.db'
    # Debugging aktivieren für die Tests
    DEBUG = True
    TESTING = True
    
