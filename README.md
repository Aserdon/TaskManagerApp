# TaskManagerApp
This is a simple task manager application built with Python's Flask framework. The app allows users to add, delete, and mark tasks as completed. Tasks are stored in an SQLite database, and the user interface is built with HTML, CSS, and Bootstrap. JavaScript is used to convert UTC time to local time.


## Technologies Used
Python: For the Flask application logic.
Flask: For routing and rendering HTML templates.
SQLite: A lightweight database for storing tasks.
HTML & CSS: For building and styling the user interface.
Bootstrap: For a fast and responsive design.
JavaScript: For converting UTC time to local time.
PyInstaller: To create an executable file.


## Installation Instructions
Clone the repository

Navigate to the project directory

Create and activate a virtual environment:
```
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

Install dependencies:
```
pip install -r requirements.txt
```

Run the application:
```
python app.py
```


## Features:
 - Add tasks
 - Delete tasks
 - Mark tasks as completed or undo completion
 - Sort tasks by alphabetical order, creation time or time of completion
 - Responsive UI using Bootstrap

 
## Testing
This project includes unit tests written using Python's unittest module. The tests verify functionality of adding and deleting task, and of setting tasks complete/incomplete.

Run the tests:
```
python -m unittest test_app.py
```

 
## Packaging as an Executable
If you'd like to create an executable file for Windows:

Install PyInstaller:
```
pip install pyinstaller
```

Build the executable:
```
pyinstaller --onefile app.py
```

This will create an executable file in the dist folder that can be shared without requiring Python to be installed.

 
## Database Setup
The app automatically creates an SQLite database file (if one doesn't already exist). You don't need to manually create the database file. However, if you'd like to reset the database, you can delete the tasks.db file in the project directory.
