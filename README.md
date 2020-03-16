## Prerequisites
1. [Python 3.6](https://www.python.org/downloads/release/python-3610/)
2. [pip](https://pip.pypa.io/en/stable/installing/)
3. [Neo4J](https://neo4j.com/download/)

## Setting up
1.Script dependencies

Simply run the shell script called `setup_env.sh`:
```bash
sh setup_env.sh
```

2.Setting up the data

For the territorial data, the script expects a number of `.csv` files to be
in the same directory:

| File name            | Meaning                        |
|----------------------|--------------------------------|
| `countries.csv`      | The countries information      |
| `regions.csv`        | The regions information        |
| `counties.csv`       | The counties information       |
| `municipalities.csv` | The municipalities information |
| `cities.csv`         | The cities information         |
| `communes.csv`       | The communes information       |

## Running the script

Once you have everything setup, you first have to make sure you're using the 
virtual environment we created at the previous step. To do that, run:

```bash
source venv/bin/activate
```

Now we're good to go. 

The database populator can be run as:
```bash
python process_csvs.py [-h] [--insert-territories] [--host HOST] 
                       [--port PORT] [--user USER] [--password PASSWORD]
                       [-v] data
```

As you can see, there are a number of options can be used. Here is what they
mean:

| Option                 | Definition                                                                                     |
|------------------------|------------------------------------------------------------------------------------------------|
| `data`                 | Path to the data directory.                                                                    |
| `-h`                   | Show the help message and exit                                                                 |
| `--insert-territories` | Whether to insert the territories as well or not. (For now only mode the script can be run in. |
| `--host HOST`          | Host where the neo4j server is running.                                                        |
| `--port PORT`          | Port where the neo4j server is running.                                                        |
| `--user USER`          | User used to connect to the neo4j server.                                                      |
| `--password PASSWORD`  | Password used to connect to the neo4j server.                                                  |
| `-v, --verbose`        | Whether to log the inner workings of the script or not.                                        |