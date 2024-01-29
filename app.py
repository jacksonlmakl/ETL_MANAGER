from flask import Flask, request, jsonify
from core import Client, newClient
import json
app = Flask(__name__)


@app.route('/create_or_load_client', methods=['POST'])
def create_or_load_client():
    data = request.get_json()
    instance_name = data.get('instance_name')
    username = data.get('username')
    password = data.get('password')
    method = data.get('method')
    # Check if the client already exists
    if method == 'load':
        client = Client(instance_name, username, password)
    elif method == 'create':
        # If not, create a new client
        client = newClient(instance_name, username, password)
    output = client.to_dict()
    return json.dumps(output)


@app.route('/create_connection', methods=['POST'])
def create_connection():
    data = request.get_json()
    instance_name = data.get('instance_name')
    username = data.get('username')
    password = data.get('password')
    connection_name = data.get('connection_name')
    connection_type = data.get('connection_type')
    account = data.get('account')
    connection_password = data.get('connection_password')
    connection_username = data.get('connection_username')

    client = Client(instance_name, username, password)
    print(client)
    client.create_connection(connection_name = connection_name,
                             connection_type = connection_type,
                             username = connection_username,
                             password = connection_password,
                             account = account)
    client.save()

    return jsonify(client.to_dict())


@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.get_json()
    instance_name = data.get('instance_name')
    username = data.get('username')
    password = data.get('password')
    project_name = data.get('project_name')

    client = Client(instance_name, username, password)
    client.create_project(project_name)
    client.save()

    return jsonify(client.to_dict())


@app.route('/create_script', methods=['POST'])
def create_script():
    data = request.get_json()
    instance_name = data.get('instance_name')
    username = data.get('username')
    password = data.get('password')
    project_name = data.get('project_name')
    script_name = data.get('script_name')
    script_code = data.get('script_code')

    client = Client(instance_name, username, password)
    project = client.get_project(project_name)
    project.create_script(script_name, script_code)
    client.save()

    return jsonify(client.to_dict())


@app.route('/create_automation', methods=['POST'])
def create_automation():
    data = request.get_json()
    instance_name = data.get('instance_name')
    username = data.get('username')
    password = data.get('password')
    project_name = data.get('project_name')
    automation_name = data.get('automation_name')
    scripts = data.get('scripts')
    order = data.get('order')
    schedule = data.get('schedule')

    client = Client(instance_name, username, password)
    project = client.get_project(project_name)
    print(scripts)
    script_objects= []
    for i in scripts:
        print(i)
        script_objects.append(project.get_script(i))
    print('script_objects asfasdfasdfsadfsdaf')
    print(script_objects)
    project.create_automation(automation_name, script_objects, order, schedule)
    client.save()

    return jsonify(client.to_dict())


@app.route('/start_automation', methods=['POST'])
def start_automation():
    data = request.get_json()
    instance_name = data.get('instance_name')
    username = data.get('username')
    password = data.get('password')
    project_name = data.get('project_name')
    automation_name = data.get('automation_name')
    connection_name = data.get('connection_name')
    client = Client(instance_name, username, password)
    project = client.get_project(project_name)
    project.start_automation(automation_name = automation_name, client_name = instance_name, username=username, connection_name=connection_name, project_name = project_name, password=password)

    client.save()
    print(client.to_dict())
    return jsonify(client.to_dict())


@app.route('/stop_automation', methods=['POST'])
def stop_automation():
    data = request.get_json()
    instance_name = data.get('instance_name')
    username = data.get('username')
    password = data.get('password')
    project_name = data.get('project_name')
    automation_name = data.get('automation_name')

    client = Client(instance_name, username, password)
    project = client.get_project(project_name)
    project.stop_automation(instance_name, username, password, automation_name)
    client.save()

    return jsonify(client.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
