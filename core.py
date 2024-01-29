import os
import snowflake.connector
import pickle
import toml
import hashlib
import secrets
from crontab import CronTab

# Define the client class
class client:
    def __init__(self, name, config_file='credentials.toml'):
        self.name = name
        self.config_file = config_file
        self.client_dir = os.path.join(os.getcwd(), name)
        if not os.path.isfile(self.client_dir):
            os.makedirs(self.client_dir, exist_ok=True)
        self.load_credentials()
        self.projects = {}
        self.connections = {}
    def load_credentials(self):
        try:
            config_data = toml.load(os.path.join(self.client_dir, self.config_file))
            self.username = config_data[self.name]['username']
            self.salt_file = os.path.join(self.client_dir, f'{self.name}_salt.txt')
            self.hashed_password_file = os.path.join(self.client_dir, f'{self.name}_hashed_password.txt')

            # Load salt from file
            with open(self.salt_file, 'r') as salt_file:
                self.salt = salt_file.read()

            # Load hashed password from file
            with open(self.hashed_password_file, 'r') as hashed_password_file:
                self.hashed_password = hashed_password_file.read()

        except (FileNotFoundError, KeyError):
            print(f"Credentials not found for client '{self.name}'. Please run 'save_credentials' first.")

    def save_credentials(self, username, password):
        self.username = username

        # Generate a new salt
        salt = secrets.token_hex(16)
        self.salt_file = os.path.join(self.client_dir, f'{self.name}_salt.txt')

        # Save salt to file
        with open(self.salt_file, 'w') as salt_file:
            salt_file.write(salt)

        # Hash the password using the generated salt
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        self.hashed_password = hashed_password

        # Save hashed password to file
        self.hashed_password_file = os.path.join(self.client_dir, f'{self.name}_hashed_password.txt')
        with open(self.hashed_password_file, 'w') as hashed_password_file:
            hashed_password_file.write(hashed_password.hex())

        config_data = {self.name: {'username': username}}
        with open(os.path.join(self.client_dir, self.config_file), 'w') as config_file:
            toml.dump(config_data, config_file)


    def verify_password(self, input_password):
        hashed_input_password = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), self.salt.encode('utf-8'), 100000)
        return hashed_input_password.hex() == self.hashed_password

    def create_connection(self, connection_name, account, connection_type, username, password):
        conn = {connection_name: connection(connection_name, account, connection_type, username, password)}
        self.connections = {**self.connections, **conn}

    def create_project(self, project_name):
        proj = {project_name: project(project_name)}
        self.projects = {**self.projects, **proj}

    def get_connection(self, connection_name):
        return self.connections[connection_name]

    def get_project(self, project_name):
        return self.projects[project_name]

    def to_dict(self):
        # Return a simplified dictionary representation of the client object
        return {
            'name': self.name,
            'username': self.username,
            'projects': {name: proj.to_dict() for name, proj in self.projects.items()},
            'connections': {name: conn.to_dict() for name, conn in self.connections.items()}
        }

    def save(self):
        filename = os.path.join(self.client_dir, f'{self.name}.pkl')
        with open(filename, 'wb') as outp:
            data = self.to_dict()
            pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)

    def load(self, input_username, input_password):
        if self.verify_password(input_password):
            filename = os.path.join(self.client_dir, f'{self.name}.pkl')
            try:
                with open(filename, 'rb') as inp:
                    data = pickle.load(inp)
                    self.from_dict(data)
                    return self
            except FileNotFoundError:
                print(f"File not found: {filename}")
        else:
            print("Invalid username or password. Loading aborted.")

    def from_dict(self, data):
        self.name = data['name']
        self.username = data['username']
        self.projects = {name: project_from_dict(proj) for name, proj in data['projects'].items()}
        self.connections = {name: connection_from_dict(conn) for name, conn in data['connections'].items()}

# Define the connection class
class connection:
    def __init__(self, name, account, connection_type, username, password):
        self.name = name
        self.connection_type = connection_type
        self.username = username
        self.password = password
        self.account = account
        self.con = snowflake.connector.connect(
            user=self.username,
            password=self.password,
            account=self.account
        )

    def Session(self):
        return session(self.con)

    def to_dict(self):
        # Return a simplified dictionary representation of the connection object
        return {
            'name': self.name,
            'connection_type': self.connection_type,
            'username': self.username,
            'password': self.password,
            'account': self.account
        }

def connection_from_dict(data):
    return connection(data['name'], data['account'], data['connection_type'], data['username'], data['password'])

# Define the session class
class session:
    def __init__(self, con):
        self.con = con
        self.cursor = self.con.cursor()

    def execute(self, code):
        return self.cursor.execute(code).fetch_arrow_all().to_pylist()

# Define the project class
class project:
    def __init__(self, name):
        self.name = name
        self.scripts = {}
        self.automations = {}

    def create_automation(self, automation_name, scripts, order, schedule):
        auto_obj = automation(automation_name, scripts, order, schedule)
        automation_instance = {automation_name: auto_obj}
        self.automations = {**self.automations, **automation_instance}

    def start_automation(self, automation_name,project_name, client_name,username,connection_name,password):
        temp_client = Client(client_name,username,password)
        print(temp_client.name)
        self.connection_name = connection_name
        print(self.automations[automation_name].scripts)

        scripts = self.automations[automation_name].scripts
        schedule = self.automations[automation_name].schedule
        order = self.automations[automation_name].order
        file_path = f'{temp_client.name}__AUTOMATION__{automation_name}.py'
        full_code = f"import sys\nimport core\ntemp_client = core.Client('{temp_client.name}','{temp_client.username}','{password}')\n"
        for order_name in order:
            for script in scripts:
                script = temp_client.get_project(project_name).get_script(script)
                if script.name == order_name:
                    code = script.code
                    line = f"""temp_client.get_connection('{self.connection_name}').Session().execute('{code}')\n"""
                    full_code = full_code + line

        with open(file_path, 'w') as file:
            file.write(full_code)
        cron = CronTab(user='jacksonmakl')
        job = cron.new(command=f'python {file_path}')
        job.minute.every(schedule)
        cron.write()
    def stop_automation(self, client_name,username,password, automation_name):
        temp_client = Client(client_name, username, password)
        file_path = f'{temp_client.name}__AUTOMATION__{automation_name}.py'
        job_command = f'python {file_path}'
        cron = CronTab(user=True)
        for job in cron:
            if job_command in job.command:
                cron.remove(job)
                cron.write()
    def create_script(self, script_name, code):
        script_instance = {script_name: script(script_name, code, self.name)}
        self.scripts = {**self.scripts, **script_instance}

    def get_script(self, script_name):
        return self.scripts[script_name]

    def get_automation(self, automation_name):
        return self.automations[automation_name]

    def to_dict(self):
        # Return a simplified dictionary representation of the project object
        scripts_dict = {}
        for name, script_obj in self.scripts.items():
            if isinstance(script_obj, script):
                scripts_dict[name] = script_obj.to_dict()
        automations_dict = {}
        for name, auto_obj in self.automations.items():
            if isinstance(auto_obj, automation):
                automations_dict[name] = auto_obj.to_dict()
        return {
            'name': self.name,
            'scripts': scripts_dict,
            'automations': automations_dict
        }

def project_from_dict(data):
    p = project(data['name'])
    p.scripts = {name: script_from_dict(script) for name, script in data['scripts'].items()}
    p.automations = {name: automation_from_dict(auto) for name, auto in data['automations'].items()}
    return p

# Define the automation class
class automation:
    def __init__(self, name, scripts, order, schedule):
        self.name = name
        self.scripts = scripts
        self.order = order
        self.schedule = schedule

    def add_script(self, script_name):
        self.scripts.append(script_name)
        self.order.append(script)

    def set_order(self, order):
        self.order = order

    def to_dict(self):
        # Convert script objects to dictionaries
        scripts_dict = {}
        for script_obj in self.scripts:
            if isinstance(script_obj, script):
                scripts_dict[script_obj.name] = script_obj.to_dict()

        # Return a simplified dictionary representation of the automation object
        return {
            'name': self.name,
            'scripts': scripts_dict,
            'order': self.order,
            'schedule': self.schedule
        }

def automation_from_dict(data):
    a = automation(data['name'], data['scripts'], data['order'],data['schedule'])
    return a

# Define the script class
class script:
    def __init__(self, name, code, project_name):
        self.project_name = project_name
        self.name = name
        self.code = code

    def modify_script(self, code):
        self.code = code

    def to_dict(self):
        # Return a simplified dictionary representation of the script object
        return {
            'name': self.name,
            'code': self.code,
            'project_name': self.project_name
        }

def script_from_dict(data):
    return script(data['name'], data['code'], data['project_name'])


def newClient(name, username, password):
    new_client = client(name)
    new_client.save_credentials(username=username,password=password)
    new_client.save()
    loaded_client = client(name).load(username,password)
    return loaded_client

def Client(name, username, password):
    loaded_client = client(name).load(username,password)
    return loaded_client



