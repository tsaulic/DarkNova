import os
import platform

import semver
from google.cloud.secretmanager_v1 import AccessSecretVersionRequest

system = platform.system()

version = semver.VersionInfo.parse('0.3.3-alpha+build.17')
if system == 'Windows' or system == 'Darwin':
    game_db_path = 'postgres+psycopg2://postgres:password@localhost:5432/darknova'
elif system == 'Linux':
    from google.cloud import secretmanager

    secrets = secretmanager.SecretManagerServiceClient()
    postgres_user = 'postgres'
    # noinspection PyTypeChecker
    project_id = '546542878411'
    # noinspection PyTypeChecker
    postgres_password = secrets.access_secret_version(AccessSecretVersionRequest(
        name=f'projects/{project_id}/secrets/postgres_password/versions/1')).payload.data.decode('utf-8')
    # noinspection PyTypeChecker
    public_ip = secrets.access_secret_version(AccessSecretVersionRequest(
        name=f'projects/{project_id}/secrets/public_sql_instance_ip/versions/1')).payload.data.decode('utf-8')
    # noinspection PyTypeChecker
    database_name = secrets.access_secret_version(AccessSecretVersionRequest(
        name=f'projects/{project_id}/secrets/db_name/versions/1')).payload.data.decode('utf-8')
    # noinspection PyTypeChecker
    cloud_instance = secrets.access_secret_version(AccessSecretVersionRequest(
        name=f'projects/{project_id}/secrets/sql_cloud_instance_name/versions/1')).payload.data.decode('utf-8')
    game_db_path = f'postgres+psycopg2://{postgres_user}:{postgres_password}@{public_ip}/{database_name}?host=/cloudsql/{cloud_instance}'

secret_key = os.environ.get('DARKNOVA_SECRET_KEY') or "test"

# game related stuff
sectors_default_amount = 500
