from RPA.Database import Database
from robocorp import vault


def connect_to_database_with_secrets():
    # Get database information from the vault
    db_info = vault.get_secret("mysql_data")

    # Connect to the database using the secrets
    db = Database()
    db.connect_to_database(
        "pymysql",
        db_info["database"],
        db_info["username"],
        db_info["password"],
        db_info["location"],
    )
    return db


def close_database_connection(database):
    database.disconnect_from_database
