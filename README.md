# cleanStorage

- **Goal**: clean-up TEMPORARY STORAGE folders. 

- **Targets**: Asiago first ingestion machine, test machines (all nodes) - more generally, all the machines that host a temporary storage. 

- **Description**: Files in the storage are selected according to their date. If older than the number of months specified in the configuration file, their checksum is calculated, compared to the value found in database and if they match, the file is removed. 

- **Configuration parameters**:

      "storage_folder": path to the storage folder to be checked 
      "months_nr": number of months within which the data needs to be preserved on the machine. Files with dates older than *today-months_nr* will be discarded.
      "db_host": IP address /name of the host containing the local database (usually localhost)
      "db_pwd": local database password
      "db_user": local database user
      "db_name": name of the local database to be queried
      "db_port": local database port
      "email": email receiving the alerts
      "sender": email sender
      "smtp_host": smtp domain of the local machine sending the email
      "db_tables": list of tables inside db_name that need to be queried

- **Requirements**:
    - python3
    - pip install astropy
    - pip install sqlalchemy
    - pip install pymysql

- **Usage**:
    - configure the conf.json file
    - /usr/bin/python main.py
