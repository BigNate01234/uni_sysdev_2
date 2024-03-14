from DatabaseHandler import DatabaseHandler
import os.path


def test_database_creation():

    # NOTE: we remove this to prevent interference from previous tests
    if os.path.isfile('test_database.db'):
        os.remove('test_database.db')

    dbh = DatabaseHandler('test_database.db')
    assert os.path.isfile('test_database.db')

    dbh.create_tables()

    schema = dbh.execute_query('PRAGMA table_info(Sales);')
    assert schema == [(0, 'id', 'INTEGER', 1, None, 1),
                      (1, 'itemid', 'INTEGER', 0, None, 0),
                      (2, 'date', 'TEXT', 0, None, 0)]

    schema = dbh.execute_query('PRAGMA table_info(Stock);')

    assert schema == [(0, 'id', 'INTEGER', 1, None, 1),
                      (1, 'name', 'TEXT', 0, None, 0),
                      (2, 'price', 'REAL', 0, None, 0),
                      (3, 'quantity', 'INTEGER', 0, None, 0),
                      (4, 'musicGroup', 'TEXT', 0, None, 0)]


def test_inserting_row():

    dbh = DatabaseHandler('test_database.db')
    dbh.execute_query(""" INSERT INTO Stock (name, price, quantity, musicGroup)
                            VALUES ('TestItemName',10,1000,'TestGroup');""")
    dbh.commit_changes()

    test_data = dbh.execute_query("""SELECT * FROM Stock
                                WHERE name='TestItemName'""")
    assert test_data == [(1, 'TestItemName', 10.0, 1000, 'TestGroup')]


def test_updating_row():

    dbh = DatabaseHandler('test_database.db')
    dbh.execute_query(""" UPDATE Stock
                      SET price=500
                      WHERE name='TestItemName';""")
    dbh.commit_changes()

    test_data = dbh.execute_query("""SELECT * FROM Stock
                                  WHERE name='TestItemName'""")
    assert test_data == [(1, 'TestItemName', 500, 1000, 'TestGroup')]


def test_delete_row():

    dbh = DatabaseHandler('test_database.db')
    dbh.execute_query("DELETE FROM Stock WHERE name='TestItemName';")

    data = dbh.execute_query("SELECT * FROM Stock WHERE name='TestItemName'")
    assert len(data) == 0
