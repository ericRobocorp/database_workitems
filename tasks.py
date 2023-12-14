from pathlib import Path

from robocorp import workitems, vault
from robocorp.tasks import get_output_dir, task
from RPA.Excel.Files import Files as Excel
from RPA.Database import Database
import random

"""name of the table hosting the data"""
TABLE = "workitems"


@task
def producer():
    """Open database connection"""
    db = connect_to_database()

    """Split Excel rows into multiple output Work Items for the next step."""
    output = get_output_dir() or Path("output")
    filename = "orders.xlsx"

    for item in workitems.inputs:
        path = item.get_file(filename, output / filename)

        excel = Excel()
        excel.open_workbook(path)
        rows = excel.read_worksheet_as_table(header=True)
        customers = rows.group_by_column("Name")
        for customer in customers:
            payload = {
                "Name": customer.get_column("Name")[0],
                "Zip": customer.get_column("Zip")[0],
                "Product": [],
            }
            for row in customer:
                payload["Product"].append(row["Item"])
            id = store_workitems_in_database(
                payload["Name"], payload["Zip"], payload["Product"], db
            )
            workitems.outputs.create(id)
    close_database_connection(db)


@task
def consumer():
    """Process all the produced input Work Items from the previous step."""
    db = connect_to_database()
    for item in workitems.inputs:
        try:
            name, zip, product = get_workitems_from_database(item.payload, db)
            # name = item.payload["Name"]
            # zipcode = item.payload["Zip"]
            # product = item.payload["Product"]
            print(f"Processing order: {name}, {zip}, {product}")
            item.done()
        except AssertionError as err:
            item.fail("BUSINESS", code="INVALID_ORDER", message=str(err))
        except KeyError as err:
            item.fail("APPLICATION", code="MISSING_FIELD", message=str(err))
    close_database_connection(db)


def connect_to_database():
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
    """Remember to always close the database connection"""
    database.disconnect_from_database


def store_workitems_in_database(name, zip_code, items, db):
    """We use the random.randint(10000, 40000) to create a random ID which will be used to recall the information in the consumer step
    Because we grouped the items to be ordered in a list of strings, we combine them into one string to be stored in the database for simplicity with the ",".joins(items) statement
    """
    random_id = random.randint(10000, 40000)
    string_items = ",".join(items)
    variables = f"('{random_id}', '{name}', '{zip_code}', '{string_items}')"
    insert = f"INSERT INTO {TABLE} (id,name,zip,items) VALUES {variables}"
    result = db.query(insert)
    return random_id


def get_workitems_from_database(id, db):
    """We retrieve the work items from the database using the {id} created when we stored them"""
    get_data = f"SELECT name, zip, items FROM {TABLE} WHERE id={id}"
    work_item = db.query(get_data)
    row = work_item.data[0]
    name = row[work_item.columns.index("name")]
    zip = row[work_item.columns.index("zip")]
    items = row[work_item.columns.index("items")]
    return name, zip, items
