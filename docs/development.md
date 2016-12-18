# How to develop
* Install python3, virtualenv, PostgreSQL and PostGIS using your package manager or manually on Windows. E.g. on Fedora: `dnf install python3 virtualenv postgresql-server postgis`
* Setup PostgreSQL, create a user with password and enabled `md5` authentication. Then create a database (`ocyco`) and activate the `postgis` extension for this database.
* Checkout sources via git. 
* Create a virtualenv in the project directory: `virtualenv-3 venv`. To activate this virtualenv use: `source venv/bin/activate`.
* Install python dependencies: `pip install -r requirements.txt`
* Copy `config.sample.py` to `config.py` and adapt to your database connection.
* `python3 ./run.py` to run the ocyco-server locally on port 5000.