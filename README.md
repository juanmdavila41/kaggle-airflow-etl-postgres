# kaggle-airflow-etl-postgres
## Overview
This project aims to create an ETL (Extract, Transform, Load) pipeline to fetch data from Kaggle using its API and subsequently load it into a PostgreSQL database. The ETL process is orchestrated using Apache Airflow, deployed within Docker containers.
## Features
- Utilizes Kaggle API to fetch data from the "prasad22/global-economy-indicators" dataset.
- Transformation of fetched data is performed using Pandas.
- Data is loaded into a PostgreSQL database.
- Dockerized deployment using Dockerfile, docker-compose, and requirements file for API installation.

## ETL Process
The ETL process is orchestrated using Airflow's Directed Acyclic Graphs (DAGs). The DAG performs the following steps:
1. Extract: Data is retrieved from Kaggle using the Kaggle API.
2. Transform: Pandas is employed to preprocess and transform the data.
3. Load: Transformed data is loaded into a PostgreSQL database.

## Database Structure
The PostgreSQL database consists of the following components:
- Temporary Table: Holds the temporary data extracted from Kaggle during each DAG execution.
- Final Table: Stores the historical real data.
- Stored Procedure: A stored procedure, created using the sp_creator.py script, facilitates merging of data between the temporary and final tables. This merge process ensures updating, ignoring, or loading new information efficiently.

## Usage
1. Clone the repository.
2. Install Docker if not already installed.
3. Navigate to the project directory.
4. Build and run Docker containers using docker-compose up.
5. Access Airflow UI to monitor and trigger the DAG for ETL execution.

## Dependencies
Ensure the following dependencies are installed:

- Docker
- PostgreSQL
- Apache Airflow
- Python (with Pandas library)

## Contributing
Contributions to enhance the project are welcomed. Feel free to submit pull requests or raise issues for any improvements or bugs.

