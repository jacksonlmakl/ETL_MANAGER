import requests
import json


class ClientAPI:
    def __init__(self, base_url='http://127.0.0.1:5000'):
        self.base_url = base_url

    def create_or_load_client(self, instance_name, username, password, method):
        data = {
            'instance_name': instance_name,
            'username': username,
            'password': password,
            'method': method
        }
        response = requests.post(f'{self.base_url}/create_or_load_client', json=data)
        return json.loads(response.text)

    def create_connection(self, instance_name, username, password, connection_name, connection_type, account,
                          connection_username, connection_password):
        data = {
            'instance_name': instance_name,
            'username': username,
            'password': password,
            'connection_name': connection_name,
            'connection_type': connection_type,
            'account': account,
            'connection_username': connection_username,
            'connection_password': connection_password
        }
        response = requests.post(f'{self.base_url}/create_connection', json=data)
        return json.loads(response.text)

    def create_project(self, instance_name, username, password, project_name):
        data = {
            'instance_name': instance_name,
            'username': username,
            'password': password,
            'project_name': project_name
        }
        response = requests.post(f'{self.base_url}/create_project', json=data)
        return json.loads(response.text)

    def create_script(self, instance_name, username, password, project_name, script_name, script_code):
        data = {
            'instance_name': instance_name,
            'username': username,
            'password': password,
            'project_name': project_name,
            'script_name': script_name,
            'script_code': script_code
        }
        response = requests.post(f'{self.base_url}/create_script', json=data)
        return json.loads(response.text)

    def create_automation(self, instance_name, username, password, project_name, automation_name, scripts, order,
                          schedule):
        data = {
            'instance_name': instance_name,
            'username': username,
            'password': password,
            'project_name': project_name,
            'automation_name': automation_name,
            'scripts': scripts,
            'order': order,
            'schedule': schedule
        }
        response = requests.post(f'{self.base_url}/create_automation', json=data)
        return json.loads(response.text)

    def start_automation(self, instance_name, username, password, project_name, automation_name, connection_name):
        data = {
            'instance_name': instance_name,
            'username': username,
            'password': password,
            'project_name': project_name,
            'automation_name': automation_name,
            'connection_name': connection_name
        }
        response = requests.post(f'{self.base_url}/start_automation', json=data)
        return json.loads(response.text)

    def stop_automation(self, instance_name, username, password, project_name, automation_name):
        data = {
            'instance_name': instance_name,
            'username': username,
            'password': password,
            'project_name': project_name,
            'automation_name': automation_name
        }
        response = requests.post(f'{self.base_url}/stop_automation', json=data)
        return json.loads(response.text)

