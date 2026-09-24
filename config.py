import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "inventory-management-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///inventory.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False