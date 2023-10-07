import unittest
import sys
import os
from unittest.mock import patch, Mock, MagicMock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import database

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_conn = Mock()
        self.mock_cursor = Mock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        database.db_pool = MagicMock()

    @patch('src.database.db_pool.getconn', return_value=Mock())
    def test_connect_db(self, mock_pool_getconn):
        conn = database.connect_db()
        self.assertIsNotNone(conn)

    @patch('src.database.db_pool.putconn')
    def test_release_conn_to_pool(self, mock_pool_putconn):
        database.release_conn_to_pool(self.mock_conn)
        mock_pool_putconn.assert_called_once_with(self.mock_conn)

    @patch('src.database.connect_db', return_value=Mock())
    def test_create_table_if_not_exists(self, mock_connect_db):
        database.create_table_if_not_exists(self.mock_conn)
        self.mock_cursor.execute.assert_called_once()

    @patch('src.database.connect_db', return_value=Mock())
    def test_insert_records(self, mock_connect_db):
        records = [('test_user', 'test_device', '127.0.0.1', 'device_id', 'en_US', '1.0.0')]
        database.insert_records(self.mock_conn, records)
        self.mock_cursor.executemany.assert_called_once()

    @patch('src.database.db_pool.closeall')
    def test_close_db_pool(self, mock_pool_closeall):
        database.close_db_pool()
        mock_pool_closeall.assert_called_once()
if __name__ == '__main__':
    unittest.main()

