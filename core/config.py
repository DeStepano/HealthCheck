import yaml

class Config(object):
    def __init__(self):
        with open("/home/sasha/health_checker/HealthCheck/core/config.yaml", "r") as file:
            data = yaml.safe_load(file)
            self.token = data['TOKEN']  
            self.rcp_client = data['rcp_client'] 
            self.host = self.rcp_client['host'] 
            self.queues = self.rcp_client['queues']
            self.brain_analysis_queue = self.queues['brain_queue']
            self.xray_queue = self.queues['xray_queue']
            self.first_check_queue = self.queues['first_check_queue']
            self.second_check_queue = self.queues['second_check_queue']


config = Config()