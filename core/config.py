import yaml

class Config(object):
    def __init__(self):
        with open("/home/sasha/health_checker/HealthCheck/core/config.yaml", "r") as file:
            data = yaml.safe_load(file)
            self.token = data['TOKEN']  
            self.rpc_client = data['rpc_client'] 
            self.rpc_host = self.rpc_client['host'] 
            self.queues = self.rpc_client['queues']
            self.brain_analysis_queue = self.queues['brain_queue']
            self.xray_queue = self.queues['xray_queue']
            self.first_check_queue = self.queues['first_check_queue']
            self.second_check_queue = self.queues['second_check_queue']
            self.fullcheck_queue = self.queues['fullcheck_queue']
            self.users_db = data['users_db']
            self.users_db_host = self.users_db['host']
            self.user_db_port = self.users_db['port']
            self.user_db_user = self.users_db['user']
            self.users_db_password = self.users_db['password']
            self.users_db_database = self.users_db['database']


config = Config()