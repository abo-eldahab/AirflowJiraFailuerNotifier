from airflow.models import DagRun
from airflow.utils.db import provide_session


@provide_session
def get_previous_dagrun_status(dag_id, execution_date, session=None):
    """
        Retrieves the status of the most recent DAG run before a given execution date.

        This function uses Airflow's database session to query the DagRun table and find
        the last run of a specified DAG that occurred before the given execution date.

        Args:
            dag_id (str): The ID of the DAG for which to retrieve the previous run.
            execution_date (datetime): The execution date of the current DAG run.
            session (Session, optional): The SQLAlchemy session to use for querying.

        Returns:
            str: The state of the previous DAG run. Returns 'success' if there is no previous run.
    """
    # Query the DagRun table to find the most recent run before the given execution date
    previous_dagrun = session.query(DagRun).filter(
        DagRun.dag_id == dag_id,
        DagRun.execution_date < execution_date
    ).order_by(DagRun.execution_date.desc()).first()

    # Return the state of the previous DAG run, or 'success' if there is no previous run
    return 'success' if previous_dagrun is None else previous_dagrun.state
