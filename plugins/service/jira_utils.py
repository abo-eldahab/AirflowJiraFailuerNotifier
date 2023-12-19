from airflow.hooks.base_hook import BaseHook
from service.utils import get_previous_dagrun_status
from jira import JIRA


def jira_connection(jira_conn_id):
    """
        Establishes a connection to Jira using the provided connection ID.

        Retrieves the connection details from Airflow's connection manager and uses them
        to establish a connection to Jira.

        Args:
            jira_conn_id (str): The connection ID for Jira as configured in Airflow.

        Returns:
            JIRA: An instance of the JIRA client.
    """
    connection = BaseHook.get_connection(jira_conn_id)
    jira_options = {'server': connection.host}
    username = connection.login
    password = connection.password
    jira_conn = JIRA(options=jira_options, basic_auth=(username, password))
    return jira_conn


def create_ticket(ticket_dict, jira_conn_id):
    """
        Creates a ticket in Jira based on the provided ticket details.

        Args:
            ticket_dict (dict): A dictionary containing the fields required to create a Jira ticket.
            jira_conn_id (str): The connection ID for Jira as configured in Airflow.
    """
    jira_conn = jira_connection(jira_conn_id)
    new_ticket = jira_conn.create_issue(fields=ticket_dict)
    print(f"Created new Jira issue: {new_ticket.key}")


def failure_jira_ticket(context, ticket_dict={}, jira_conn_id='jira_conn'):
    """
        Creates a Jira ticket on the failure of an Airflow DAG.

        This function is intended to be used as a failure callback in Airflow DAGs. It checks
        if the DAG was externally triggered and if the previous run was successful before creating a ticket.

        Args:
            context (dict): The context passed by Airflow to the failure callback function.
            ticket_dict (dict, optional): A dictionary to specify additional Jira ticket fields.
            jira_conn_id (str, optional): The connection ID for Jira as configured in Airflow.
    """
    dag_run = context['dag_run']
    dag_id = context.get('dag').dag_id
    execution_date = context.get('execution_date')

    # Create a ticket only if the DAG was not externally triggered and the previous run was successful
    if not dag_run.external_trigger and get_previous_dagrun_status(dag_id, execution_date) == 'success':
        ticket_dict['summary'] = f"Failure in DAG {dag_id}"
        ticket_dict['description'] = f"""
                        *Task*: {context.get('task_instance').task_id}
                        *Execution Time*: {execution_date}
                        *Log Url*: {context.get('task_instance').log_url}
                    """
        create_ticket(ticket_dict, jira_conn_id)
