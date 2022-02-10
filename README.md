# challenge12345678

## Tech Stack

- Python (v3.6+ is required) ([download](https://www.python.org/downloads/) if required)
- [FastAPI](https://fastapi.tiangolo.com/): framework for building Python APIs
- [SQLAlchemy](https://www.sqlalchemy.org/): SQL toolkit for Python
- [SQLite3](https://docs.python.org/3/library/sqlite3.html): built-in Python library for providing a local disk-based database
- [Pytest](https://docs.pytest.org/en/7.0.x/): Python testing framework

## Set Up Virtual Environment

- Make sure you have Python 3.6+ installed.
- Open your Terminal (or Windows equivalent).
- Check if you have the package `virtualenv` installed:
  > `pip3 list`
- If not you can install it:
  > `pip install virtualenv`.
- Clone this repository onto your computer and `cd` into the folder.
- Now create a virtual environment inside the folder:
  > `python3 -m venv .env`
- Activate the virtual environment you just created:
  > `source .env/bin/activate`
- Installed the required packages:
  > `pip3 install -r requirements.txt `

## Database and Sample Data

- The API uses a local SQLite database (`database.db` file) which I have prepopulated with some sample data to play around with.
- I have provided CSVs of the sample data in these tables in the `sample_data` folder.
- The database contains two tables:
  - `sensors`: contains sensor data
  - `weatherdata`: contains weather data
- You can view the database tables with these tools:
  - [DB Browser for SQLite](https://sqlitebrowser.org/). Instructions:
    - Open DB Browser for SQLite
    - Click `Open Database` inside the application
    - Select the `database.db` file
  - [SQLite extension](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite) if using VSCode.

## Running the API

- Run the API with:
  > `uvicorn main:app`
- This should run the application on localhost: 
  > http://127.0.0.1:8000

## Interacting with the API

- FastAPI comes with an interactive API documentation and exploration web UI that allows you to call and test the API directly from the browser. 
  - [Link](https://fastapi.tiangolo.com/features/#automatic-docs) to FastAPI docs detailing this feature.
  - I recommend using this method to interact with the API.
  - Whilst the API running, access the interactive playground by opening localhost:
    > http://127.0.0.1:8000/docs#/
- Alternatively, you can use a tool like [Postman](https://www.postman.com/downloads/) to interact with the API.

## Testing

- Test coverage for this application is currently at 99%.
- You can run the unit tests with the following:
  > `pytest -v --cov-report term --cov-report html  --cov=./ test_main.py`
- This will give you a breakdown of the coverage for each file.
- It will also generate a folder called `htmlcov` that will contain an `index.html` file. You can open this file in your browser for a more detailed breakdown of the test coverage.

## Note

- Feel free to reach out if having issues with setting this up but should be fairly straightfoward :)