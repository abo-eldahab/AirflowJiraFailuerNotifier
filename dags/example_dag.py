from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from service.jira_utils import failure_jira_ticket

# Jira connection ID as configured in Airflow
JIRA_CONN_ID = 'jira_conn'

# Dictionary to define the structure of the Jira ticket to be created
ticket_dict = {
    'project': {'key': 'AIR'},
    'issuetype': {'name': 'Task'},
}

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 18),
    # Using a lambda function to pass additional arguments to the failure callback
    'on_failure_callback': lambda context: failure_jira_ticket(context, ticket_dict, JIRA_CONN_ID)
}


def my_task():
    """
        A sample task that always fails.

        Raises:
            ValueError: To simulate a task failure.
    """
    raise ValueError('Force Fail')


dag = DAG('example_dag', default_args=default_args, catchup=False, schedule_interval='*/5 * * * *')

task = PythonOperator(
    task_id='my_task',
    python_callable=my_task,
    dag=dag
)
