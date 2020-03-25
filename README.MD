# Oracle runner
Oracle runner project is intended to provide robust, secure and genenric interface to execute SQL queries on oracle database.

* [Usage](docs/usage.md)
* [Core implementation](docs/core.md)
* [Contribution guidelines](docs/guidelines.md)
* [External libraries](docs/external.md)
* [Scripts](docs/scripts.md)

### Pre-requisites
This project is developed on `python 3.6.9`. Any python interpreter `3.6.x` and above would be neccesary. python package manager `pip` would be required to install additional [external modules](docs/external.md).   

```
root@ec1d6dc413a6:# python --version
Python 3.6.9
root@ec1d6dc413a6:# pip --version
pip 20.0.1 from /lib/python3.6/site-packages/pip (python 3.6) 
```

### Testing connection to the database

Go to the same directory level as `main.py` and invoke python interpreter command line.
```
$  python
```
Once done you'll be in python command line interface. run following commands one by one.
```
$ from main import Runner
$ runner_object = Runner()
$ runner_object.test_connection()
```

Example for connection testing.
```
 root@ec1d6dc413a6:/Shared/OKR/oracle-runner-py3.6# python 
Python 3.6.9 (default, Nov  7 2019, 10:44:02) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from main import Runner
>>> runner_obj = Runner()
>>> runner_obj.test_connection()
Connection Test Succesful.
True
```

### Run custom scripts from `scripts` directory
The whole idea of this project is to provide the interface for custom scripts to be able to run oracle queries in the restrictive and agile manner.
 
 **Imporatant: Any script execution has to be called from the root of the project**
 ```
root@ec1d6dc413a6:# python scripts/test_database_connection.py 
Connection Test Succesful.
 ```

 ```
 root@ec1d6dc413a6:# python scripts/test_database_connection.py -DB_USERNAME system -DB_PASSWORD ******** -SID XE
Connection Test Succesful.
 ```