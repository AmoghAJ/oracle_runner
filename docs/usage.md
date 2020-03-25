# Oracle runner Usage

Oracle runner provides the interface to execute queries on Oracle database.   
Execution on the queries can be performed through `main.py`

by default method `exeucte()` is used to execute database query.    
For testing database connection `test_connection()` can be used.

### Running query from custom script

1. Import `Runner` class in your custom script.  
    ```
    from main import Runner
    ```
2. Create object of `Runner` class.
    ````
    runner_object  =  Runner()
    ````
    if you don't pass any argument to `Runner()` it will fetch the configuration for the default value for `environment` which is defined in `conf/configuration.ini`. This value can be overwritten if required, as follows.
    ```
    runner_object  =  Runner('PROD')
    ```
    > environment can only be LOCAL, TEST, QA, PROD
3. Execute Query.
    ````
    runner_object.execute('SLECT * from EMPLOYEES')
    ````
    > if you run select query , above method will return value in tuples. if the query if insert, update it will not return any value but, it will perform commit.