import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import connect_db, insert_records, close_db, create_table_if_not_exists
from src.credentials import get_db_params
from src.maskpii import mask_data, flatten_json

class TestDatabaseFunctions(unittest.TestCase):
    
    def test_connect_db(self):
        db_params = get_db_params()
        conn = connect_db(db_params)
        self.assertIsNotNone(conn)
        conn.close()

    def test_insert_data(self):
        db_params = get_db_params()
        conn = connect_db(db_params)
        cur = conn.cursor()  # Create a cursor from the connection
        create_table_if_not_exists(conn)

        raw_data = {
            'user_id': 'test_user',
            'device_type': 'test_device',
            'ip': '127.0.0.1',
            'device_id': 'test_device_id',
            'locale': 'en_US',
            'app_version': '1.0.0'
        }

        # Mask and flatten the data
        masked_data = mask_data(raw_data)
        flattened_data = flatten_json(masked_data)

        record_tuple = tuple(flattened_data.values())

        with conn.cursor() as cur:
            create_table_if_not_exists(conn)
            insert_records(conn, [record_tuple])
            cur.execute("SELECT * FROM user_logins WHERE user_id = %s", ('test_user',))
            result = cur.fetchone()
            self.assertEqual(result[0], 'test_user')
            cur.execute("DELETE FROM user_logins WHERE user_id = %s", ('test_user',))  # Move DELETE to the top
            conn.commit()  # Commit the DELETE operation



if __name__ == '__main__':
    unittest.main()

