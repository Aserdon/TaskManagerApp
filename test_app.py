import unittest
import os
import sqlite3
from app import app, init_db

class TaskManagerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the testing environment and initialize the database."""
        cls.app = app.test_client()
        cls.app.testing = True
        cls.db_path = os.path.join('instance', 'tasks.db')
        os.environ["FLASK_DATABASE"] = cls.db_path
        cls._init_db()

    @classmethod
    def _init_db(cls):
        """Initialize the database with the schema."""
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
        init_db(schema_file='schema.sql')

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests are complete."""
        # Ensure any lingering database connections are closed
        try:
            conn = sqlite3.connect(cls.db_path)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")

        # Delete the database file
        if os.path.exists(cls.db_path):
            try:
                os.remove(cls.db_path)
            except Exception as e:
                print(f"Could not delete database file: {e}")

    def setUp(self):
        """Set default session values before each test."""
        with self.app.session_transaction() as session:
            session['sort_incomplete'] = 'created_at'
            session['sort_completed'] = 'created_at'

    def tearDown(self):
        """Clear the tasks table and ensure the database connection is closed."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM tasks')
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error clearing tasks table: {e}")
        finally:
            try:
                conn.close()
            except UnboundLocalError:
                # Handle the case where `conn` may not have been initialized
                pass

    def test_add_task(self):
        """Test adding a task."""
        self.app.post('/add', data={'task': 'Test task'})
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            tasks = conn.execute('SELECT * FROM tasks WHERE content = ?', ('Test task',)).fetchall()
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]['content'], 'Test task')

    def test_delete_task(self):
        """Test deleting a task."""
        self.app.post('/add', data={'task': 'Test task'})
        self.app.post('/delete/1', data={})
        with sqlite3.connect(self.db_path) as conn:
            tasks = conn.execute('SELECT * FROM tasks WHERE id = 1').fetchall()
            self.assertEqual(len(tasks), 0)

    def test_toggle_task(self):
        """Test toggling a task's completion status."""
        self.app.post('/add', data={'task': 'Test task'})
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            task = conn.execute('SELECT * FROM tasks WHERE content = ?', ('Test task',)).fetchone()
            task_id = task['id']

        self.app.post(f'/toggle/{task_id}', data={})
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
            self.assertIsNotNone(task)
            self.assertEqual(task['completed'], 1)

    def test_sort_tasks(self):
        """Test sorting tasks by content."""
        self.app.post('/add', data={'task': 'B task'})
        self.app.post('/add', data={'task': 'A task'})

        response = self.app.get('/?sort_incomplete=content')
        self.assertTrue(response.data.index(b'A task') < response.data.index(b'B task'))


if __name__ == '__main__':
    unittest.main()
