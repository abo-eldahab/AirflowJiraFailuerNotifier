# Airflow Failure Handling Pipeline with Jira Integration

## Overview
This project implements an Apache Airflow pipeline that creates a Jira ticket automatically upon DAG failure, unless the DAG was manually triggered. The implementation includes custom Python scripts integrated into Airflow's Docker environment.

## Features
- **Automatic Jira Ticket Creation**: Automatically creates a Jira ticket under a specified project with predefined properties when a DAG fails.

## Prerequisites
- [Docker and Docker Compose](https://www.docker.com/get-started) installed on your system.
- Access to a [Jira instance](https://www.atlassian.com/software/jira) with the necessary permissions for creating tickets and managing projects, such as an account with email and token for authentication.

## Configuration
1. **Docker Compose Setup**:
   - The `docker-compose.yaml` file used for setting up the Airflow environment is based on the [official Apache Airflow Docker Compose template](https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml). This file has been downloaded and updated to include the necessary configurations and connections specific to this project.

2. **Environment Variables**:
   - Configure the `.env` file to specify necessary libraries (such as `jira`) in the `_PIP_ADDITIONAL_REQUIREMENTS` variable.

3. **Airflow Connections**:
   - Airflow connections needed for Jira integration and other functionalities are automatically configured via the `docker-compose.yaml` file.
   Update Airflow with valid credentials for Jira and other necessary connections.

   #### Option 1: Using `airflow_connections.sh` Script
   1. Update the `airflow_connections.sh` script with valid credentials.
   2. Run the script to automatically set up the necessary connections in Airflow.
   
   #### Option 2: Using Airflow Web UI
   1. After starting the containers, go to the Airflow Web UI.
   2. Navigate to 'Admin' > 'Connections'.
   3. Manually update or add new connections with valid credentials.

## Step 3: Usage

Deploy your DAGs and related scripts using the following steps:

1. **Start Airflow Services**:
   - Run the command `docker-compose up -d` from the directory containing the `docker-compose.yaml` file. This will start the Airflow environment.
   - Access the Airflow Web UI at `http://localhost:8080`.
   - Upon DAG failure, a Jira ticket will be created, which can be verified in your Jira instance.

2. **Project Directory Structure**:
   - Ensure your project follows the below directory structure:
     ```
     AirflowJiraFailuerNotifier/
     ├── config/
     ├── dags/
     │   └── example_dag.py
     ├── logs/
     ├── plugins/
     │   └── service/
     │       ├── jira_utils.py
     │       └── utils.py
     ├── .env
     ├── airflow_connections.sh
     └── docker-compose.yaml
     ```
- `jira_utils.py`: Functions for interacting with the Jira API.
- `utils.py`: General utility functions for the project.
- `example_dag.py`: An example DAG demonstrating failure handling and Jira ticket creation.
- `.env`: An environment file used to set necessary environment variables for the Docker Airflow setup. This includes variables for Jira integration and other Airflow configurations.
- `airflow_connections.sh`: A shell script for setting up Airflow connections. This script automates the configuration of connections needed for Airflow to interact with external services like Jira.
- `docker-compose.yaml`: The Docker Compose configuration file used to set up the Airflow environment. Originally sourced from the [official Apache Airflow Docker Compose template](https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml) and modified to include project-specific settings and connections.
