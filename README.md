# cleanStorage

- **Goal**: clean-up TEMPORARY STORAGE folders. 

- **Targets**: Asiago first ingestion machine, test machines (all nodes) - more generally, all the machines that host a temporary storage. 

- **Description**: Files in the storage are selected according to their date. If older than the number of months specified in the configuration file, their checksum is calculated, it is compared to the value found in database and if they match, the file is removed. 

- **Configuration parameters**:

      **storage_folder** [string]: path to the storage folder root  
      **months_nr" [unsigned short]: number of months. Files with dates older than *today-months_nr* will be discarded.
      **db_host** [string]: IP address / hostname of the host containing the local database (usually localhost)
      **db_pwd** [string]: local database password
      **db_user** [string]: local database user
      **db_name** [string]: name of the local database to be queried
      **db_port** [unsigned long]: local database port
      **email** [string]: email receiving the alerts
      **sender** [string]: email sender
      **smtp_host** [string]: smtp domain of the local machine sending the email
      **db_tables** [string vector]: list of tables inside db_name that need to be queried

- **Requirements**:
    - python3
    - pip3 install --user astropy
    - pip3 install --user sqlalchemy
    - pip3 install --user pymysql

- **Usage**:
    - configure the conf.json file
    - /usr/bin/python3 main.py
