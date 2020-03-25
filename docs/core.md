# Core implementation of Oracle runner
### Project structure:
```
.
|-- README.MD
|-- blacklisted_tables
|-- conf
|   |-- configuration.ini
|   |-- local.config
|   `-- sample.config
|-- docs
|   |-- core.md
|   |-- external.md
|   |-- guidelines.md
|   |-- scripts.md
|   `-- usage.md
|-- lib
|   |-- config-parser
|   |   `-- config_parser.py
|   `-- oracle-runner
|       `-- oracle_runner.py
|-- logs
|-- main.py
|-- requirement.txt
|-- scripts
|   |-- enviornment_setter.py
|   `-- test_database_connection.py
```
### Libraries
Libraries are structured as shown below:
```
lib/
|-- config-parser
|   `-- config_parser.py
`-- oracle-runner
    `-- oracle_runner.py
```
There are two major libaries `config_parser` and `oracle_runner` which are fully responsible for every execution in the project.

##### config_parser
As name suggest this library is responsible for parsing the config files from `conf` directory. This library also parses the config files which content sensetive data `username`, `password`, `SID`.

##### oracle_runner
This library is core executor of this project. it uses a external module `cx_Oracle` to perform most of the tasks mentioned below: 
* Creating connection to database
* Creating and maintaining sessions 
* Creating cursors 
* Identify query type and decide whether to return data or commit.
* Avoiding query execution on blacklisted tables.
* Running queries
* Destorying cursor, closing connection

> **Important**: We are assuming the existance of `tnsnames.ora` under the $ORACLE_HOME.

### main.py
This is a most imporant class file for oracle runner. Parsing the configuration and oracle query execution is done from here. This is wrapper class which resides in the root directory of the project, which internally creates objects of the classes from the class files under `lib` directory.

How to use `main.py` as a wrapper for your custom scripts? [click here](usage.md)

### Black listed tables
In order to limit the execution of any sql query on table which has high sensetive data, this file has been maintained. Any table mentioned in this file will be restricted by oracle runner to run any query. It is a simple text file where table names are written on every new line.     
**filename**: [blacklisted_tables](../blacklisted_tables)

### Scripts
Custom scripts can be written and stored [scripts](../scripts/) directory. This scripts can contain some additional buisness logic, some validations, argument parameters and call to oracle runner execution class method.

any script should run thorugh root directory of project.
```
$ python scripts/test_database_connection.py
```

Every script should contain following lines of code inorder rightly identify the dependancies.
```
from enviornment_setter import set_enviornment
set_enviornment()
```
[`enviornment_setter.py`](../scripts/enviornment_setter.py) file holds the function `set_enviornment()`, which sets the dependacies correctly for your custom scripts.

> Multiple queries can be run parallel using multi threading concept, where multiple object query execute method or oracle runner class is invloked.

### Configuration
Configration related to this project can be found under `conf` directory. Base configuration can be found in `configuration.ini`. This configuration is parsed using [configparser](https://docs.python.org/3/library/configparser.html) module of python.

```
[config-file-path]
DEV=foo/bar.config
SAMPLE=conf/sample.config

[default-config-headers]
USERNAME_CONFIG_HEADER=DatabaseUser
PASSWORD_CONFIG_HEADER=DatabasePassword
SID_CONFIG_HEADER=DatabaseTNS

[environment]
default=DEV

[log-path]
default=logs
```
1. **config-file-path**:  absolute path to config file which contains senetive data such as database username, password and SID.
2. **default-config-headers**: config files which contains sensetive infromation has a certain structure already setuped and maintained, This files are in use for other projects too. This files has some default headers as mentioned in config.
3. **enviornment**: Here default enviornment for project can be set. once it is set, python interpritter will try to fetch all infromation related for the given enviornment like `config-file-path` etc.
4. **log-path**: by default logs are directed to `logs` directory. you can set value to any specific directory.

### Config files
Config files which holds the sensetive data has to be in the format as specified. You can refer sample example `conf/sample.config`
```
DatabaseUser=foo
DatabasePassword=bar
DatabaseTNS=SYSTEM
```


### requirement.txt
This file contains the additional dependancy modules which are required for succesful execution of the project. `pip` package manager can be used to install additional dependancies.
```
$ pip install -r requirement.txt
```

### logs
This is the default directory for logs. logs are generated for every method invocation of `Runner`class from `main.py`.

Log level is default set to `INFO`. it is defined in `lib/oracle_runner.py` file with a class variable `DEFAULT_LOG_LEVEL`.
#### logs naming convention       
Syntax: `YYYYMMDD-HHMMSS-oracle-runner.log`   
Example: **log generated for script ran on 01.01.2020 at 10AM**: `20200101-100000-oracle-runner.log`

```
10:00:00,000 root INFO Query header: select, Return output: True
10:00:00,000 root INFO Connection established to the database. connection string: system/********@XE
10:00:00,000 root INFO Database cursor created.
10:00:00,000 root INFO Query executed: SELECT 1 FROM DUAL
10:00:00,000 root INFO Data succesfully fetched from database.
10:00:00,000 root INFO database cursor destroyed.
10:00:00,000 root INFO database connection closed.

```

### Documentation
##### README.MD
This is index page for documentation, all the neccesary information related to project can be found here. This page has multiple hyperlink to various pages which can be found under `docs` folder.
```
docs/
|-- core.md
|-- external.md
|-- guidelines.md
|-- scipts.md
`-- usage.md
```