import os
import pg8000
import sqlalchemy as sa
from constants import ENV_FILE_PATH, PRODUCTION_MODE
from dotenv import load_dotenv
import pycountry_convert as pc
from google.cloud.sql.connector import Connector, IPTypes
from google.cloud import secretmanager

# create client to access GCP secret manager
gcp_secret_mgr_client = secretmanager.SecretManagerServiceClient()

# load environment variables
load_dotenv(ENV_FILE_PATH)

project_id = os.environ["C4AI_PROJECT_ID"]
app_environment = os.environ["APP_ENVIRONMENT"]


def get_secret_value(secret_id: str, version_id: str = "latest") -> str:
    """Get the value of a secret based on secret id & version id stored in GCP Secrets Manager.

    Args:
        secret_id (str): Name of the secret or ID in GCP Secrets Manager
        version_id (str, optional): The version number of the secret. Defaults to "latest".

    Returns:
        str: Return the value of the secret corresponding to the given secret id.
    """

    # define name of the secret
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    # access the value of the given `secret version`
    response = gcp_secret_mgr_client.access_secret_version(name=name)
    # decode value of the response of `client.access_secret_version`
    secret_value = response.payload.data.decode("UTF-8")
    return secret_value


def connect_to_db_with_connector() -> sa.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.

    Returns:
        sa.engine.base.Engine : SQLAlchemy engine object using which we connect to the Cloud SQL DB
    """

    if app_environment == PRODUCTION_MODE:
        # get environment variable values from GCP Secret Manager
        db_user = get_secret_value(secret_id=os.environ["DB_USER"])
        db_pass = get_secret_value(secret_id=os.environ["DB_PASS"])
        db_name = get_secret_value(secret_id=os.environ["DB_NAME"], version_id="1")
        instance_connection_name = get_secret_value(
            secret_id=os.environ["INSTANCE_CONNECTION_NAME"]
        )
    else:
        print("load local environment variables")
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ["DB_NAME"]
        instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    ip_type = IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    # use Cloud SQL Python Connector object to connect to Cloud SQL instance
    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # create engine for connecting to PostgreSQL DB using `pg8000` driver
    pool = sa.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return pool


def convert_country_to_continent(country_name: str) -> str:
    """Get the continent name based on the given `country_name`

    Args:
        country_name (str): The name of the country of a user

    Returns:
        str: The name of the continent of the user
    """
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(
        country_continent_code
    )
    return country_continent_name
