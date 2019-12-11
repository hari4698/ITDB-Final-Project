# USA Powerplant Administration System

Members

- Atish Jain (jainm2)
- Hariharan Sreenivas (sreenh)

## Downloading the Datasets

All the required datasets can be found in the GitHub repository under the folder "Dataset".

## Setting up the System

### Postgres

Login as 'Postgres' using:

```
psql -U postgres
```

After logging in run the following code:

```postgresql
CREATE USER plantadmin WITH PASSWORD 'theadminoftheplant';
CREATE DATABASE powerplant;
GRANT ALL PRIVILEGES ON DATABASE powerplant TO plantadmin;
```

Use `\q` or `\quit` to exit and the Schema can be created using 

```
psql -U plantadmin powerplant < schema_Atish_Hariharan.sql
```

Loading the data:

The following Python package is required:
`pip install psycopg2`

The data can be loaded by running 'load_data.py' available in the GitHub repository.

### Angular

The code for Angular is under the `bolt` folder in the GitHub repository

Run the code below:

```
npm install -g @angular/cli

cd bolt

ng serve 
```
The service will be hosted here: `http://localhost:4200/`

### Python Flask

The following packages are required to run Flask

```
pip install flask
pip install flask_restful
pip install flask_cors
pip install flask_jsonpify
```

### Other Python packages

```
pip install pymongo
pip install simplejson
```
