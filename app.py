import os
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection, init_db
from utils import get_base_path

# Get the base path for the application
BASE_PATH = get_base_path()

app = Flask(__name__)

# Set a secure, randomly generated secret key in production
app.secret_key = 'legion'

@app.route('/')
def index():
    """
    Renders the main page, showing incomplete and completed tasks,
    sorted based on user preferences stored in the session.
    """
    # Initialize default sorting options if not set
    session.setdefault('sort_incomplete', 'created_at')
    session.setdefault('sort_completed', 'created_at')

    # Update sorting options based on URL parameters
    sort_incomplete = request.args.get('sort_incomplete')
    sort_completed = request.args.get('sort_completed')
    if sort_incomplete:
        session['sort_incomplete'] = sort_incomplete
    if sort_completed:
        session['sort_completed'] = sort_completed

    # Validate sorting options against allowed columns
    valid_columns = {'created_at', 'content', 'completed_at'}
    sort_incomplete = session['sort_incomplete'] if session['sort_incomplete'] in valid_columns else 'created_at'
    sort_completed = session['sort_completed'] if session['sort_completed'] in valid_columns else 'created_at'

    # Retrieve tasks from the database using sorting options
    conn = get_db_connection()
    tasks = conn.execute(
        f'SELECT * FROM tasks WHERE completed = 0 ORDER BY {session["sort_incomplete"]} ASC'
    ).fetchall()
    completed_tasks = conn.execute(
        f'SELECT * FROM tasks WHERE completed = 1 ORDER BY {session["sort_completed"]} ASC'
    ).fetchall()
    conn.close()

    return render_template('index.html', tasks=tasks, completed_tasks=completed_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """
    Adds a new task to the database and redirects to the main page.
    """
    task = request.form.get('task')
    if task:
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO tasks (content) VALUES (?)', (task,))
            conn.commit()
        finally:
            conn.close()
    return redirect(url_for('index', sort_incomplete=session['sort_incomplete'], sort_completed=session['sort_completed']))

@app.route('/delete/<int:task_id>', methods = ['POST'])
def delete_task(task_id):
    """
    Deletes a task by ID and redirects to the main page.
    """
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index', sort_incomplete=session['sort_incomplete'], sort_completed=session['sort_completed']))

@app.route('/toggle/<int:task_id>', methods = ['POST'])
def toggle_task(task_id):
    """
    Toggles the completion status of a task and updates the timestamp.
    """
    conn = get_db_connection()
    try:
        task = conn.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if task:
            if task['completed'] == 1:
                conn.execute('UPDATE tasks SET completed = 0, completed_at = NULL WHERE id = ?', (task_id,))
            else:
                conn.execute('UPDATE tasks SET completed = 1, completed_at = CURRENT_TIMESTAMP WHERE id = ?', (task_id,))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index', sort_incomplete=session['sort_incomplete'], sort_completed=session['sort_completed']))

def open_browser():
    """
    Opens the default web browser to the application's URL.
    """
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Initialize the database if it does not exist
    if not os.path.exists('instance/tasks.db'):
        init_db()
    open_browser()
    app.run(debug=False)
