
from enti.settings import AppConfig
import requests
from enti.extensions import log
import os


class SynicAPI:
    """
    Synic API Functions
    """

    EE_PIPELINE_NAME = 'externalEntityPipeline'
    ENTITY_SCHEMA_ENGINE = 'resources/default/engines/entities-1.1.1.engine'

    @staticmethod
    def synthesys_url():
        """Parses Synthesys URL"""

        def check_null(string):
            """Converts empty strings to None"""
            if isinstance(string, str):
                if len(string) > 0:
                    return string

        def parse_bool(string):
            """Converts string bool values to Booleans"""
            if isinstance(string, str):
                return string.lower() in ['true', '1', 'yes', 'y']
            return False

        host = check_null(AppConfig.SYNTHESYS_HOST)
        port = check_null(AppConfig.SYNTHESYS_PORT)
        ssl = parse_bool(AppConfig.SYNTHESYS_SSL)
        user = check_null(AppConfig.SYNTHESYS_USER)
        pswd = check_null(AppConfig.SYNTHESYS_PASS)

        if host is None:
            raise Exception('Synthesys Host has not been set.')

        protocol = 'https' if ssl else 'http'
        auth_prefix = '' if user is None or pswd is None else '{}:{}@'.format(user, pswd)
        port_suffix = '' if port is None else ':{}'.format(port)

        synthesys_url = '{}://{}{}{}/'.format(protocol, auth_prefix, host, port_suffix)

        return synthesys_url

    @staticmethod
    def synic_api_url(endpoint=''):
        """Builds the Synic API URL"""
        return '{}{}{}'.format(SynicAPI.synthesys_url(),'synic/api/', endpoint)

    @staticmethod
    def check_connection():
        """Checks Synthesys Connection"""
        try:
            r = requests.get(SynicAPI.synic_api_url('app'))

            if r.status_code == 200:
                response = r.json()
                log.debug('Synic API Version: {}'.format(response.get('version')))
                return response

            else:
                raise Exception('Synic API connection health check returned code {}'.format(r.status_code))

        except Exception as e:
            print(str(e))
            raise e

    @staticmethod
    def get_knowledge_graphs():
        """Retrieves Knowledge Graphs from Synthesys"""
        SynicAPI.check_connection()

        try:
            r = requests.get(SynicAPI.synic_api_url('kb'))

            if r.status_code == 200:
                response = r.json()

                kg_list = []

                for kg in response:
                    name = kg.get('name')
                    if name is not None:
                        kg_list.append(name)

                log.debug('Synic API /kb response', extra=kg_list)
                return kg_list

            else:
                raise Exception('Synic API List Knowledge Graphs request returned code {}'.format(r.status_code))

        except Exception as e:
            print(str(e))
            raise e

    @staticmethod
    def get_applications():
        """Retrieves Synthesys Application list"""
        SynicAPI.check_connection()

        try:
            r = requests.get(SynicAPI.synic_api_url('application'))

            if r.status_code == 200:
                response = r.json()
                applications = {a['name']:a for a in response}
                log.debug('Synic API /application count: {}'.format(len(applications)))
                return applications

            else:
                raise Exception('Synic API List Applications request returned code {}'.format(r.status_code))

        except Exception as e:
            print(str(e))
            raise e

    @staticmethod
    def has_ee_pipeline():
        """Checks Synthesys for External Entity Pipeline"""
        applications = SynicAPI.get_applications()
        is_present = applications.get(SynicAPI.EE_PIPELINE_NAME) != None
        log.debug('EE Pipeline is present: {}'.format(is_present))
        return is_present

    @staticmethod
    def ingest(kg_name, test=False):
        """Ingests an exported Entities XML file into Synthesys

        :param kg_name: Name of the Knowledge Graph to ingest into
        :param test: Test parameter used to bypass function
        :return: Task ID of the resulting process
        """
        export_filename = os.path.join(AppConfig.INSTALL_DIR, AppConfig.RELATIVE_EXPORT_FILE)
        log.debug('Absolute path of export file on host machine: {}'.format(export_filename))

        if not SynicAPI.has_ee_pipeline():
            raise Exception('Synthesys instance is missing the External Entity Pipeline')

        params = {
            'kb': kg_name,
            'process_type': 'jet',
            'application': SynicAPI.EE_PIPELINE_NAME,
            'invocationConfig': {
                'input': export_filename,
                'schemaResource': SynicAPI.ENTITY_SCHEMA_ENGINE,
                'kgName': kg_name
            }
        }

        if test:
            log.debug('*** API Request to /process endpoint is being simulated ***')
            response = {
                "id": "test-request",
                "kb": kg_name,
                "application": "externalEntityPipeline",
                "applicationReadableName": "externalEntityPipeline",
                "processType": "jet",
                "username": AppConfig.SYNTHESYS_USER,
                "requestedTime": "2018-04-16T19:47:39.563Z",
                "startedTime": None,
                "completedTime": None,
                "status": "PENDING",
                "steps": [],
                "failure": None,
                "invocationConfig": {
                    "input": export_filename,
                    "schemaResource": SynicAPI.ENTITY_SCHEMA_ENGINE,
                    "kgName": kg_name
                },
                "stackTrace": None,
                "allowedCommands": [
                    "CANCEL",
                    "CANCEL"
                ],
                "issuedCommand": None
            }
        else:
            r = requests.post(SynicAPI.synic_api_url('process'), data=params)
            if r.status_code == 200:
                response = r.json()
            else:
                raise Exception('Synic API EE Ingestion request returned code {}'.format(r.status_code))

        task_id = response.get('id')
        if task_id is None:
            raise Exception('Synic API EE Ingestion response is missing Task ID')

        extra = {
            'request': params,
            'response': response,
            'task_id': task_id
        }

        log.debug('Synic API /process request', extra=extra)

        return task_id

if __name__ == "__main__":
    #get_knowledge_graphs()
    #has_ee_pipeline()
    SynicAPI.ingest('test_kg', test=True)
