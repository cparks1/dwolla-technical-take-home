# Dwolla Technical Take Home
## RESTful API for Time with Timezone Offset
This repository contains a Flask application implementing a simple RESTful API to retrieve the current time in UTC format and optionally adjust it to a provided timezone.

# Installation
To run the application, you'll need Python 3 and pip (the Python package manager) installed on your system. You can follow the official instructions for installation here: https://www.python.org/downloads/

Once you have Python and pip set up, clone this repository and navigate to the project directory. Then, install the required dependencies using the following command:
```
pip install -r requirements.txt
```

# Running the Flask App
After installing the dependencies, you can run the Flask application in development mode using the following command:
```
python main.py
```

This will start the Flask development server, typically accessible at `http://127.0.0.1:5000/` (localhost port 5000) by default. You can then test the API using tools like Postman or by sending requests directly through your browser.

**Note:** In production environments, you'll want to set the `DEBUG_MODE` environment variable to `FALSE`.

# Running Unit Tests
The project includes unit tests written using the pytest framework. To run the tests, ensure you have pytest installed (pip install pytest). Then, from the project directory, run the following command:
```
pytest test/tests.py
```
This will execute the tests, and report the results of the tests.

# Why Flask?
Flask, a popular microframework for building web applications in Python, was chosen for this project due to its lightweight nature and ease of use. For a simple API like this, Flask provides a clear and concise way to define API endpoints and handle requests. Additionally, Flask is well documented and has a large community, making it easier to debug issues and research best practices.

For more complex APIs requiring more demanding features and functionalities, it would be worth considering other frameworks such as Django or FastAPI.