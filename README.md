## ETL Manager

This project provides functionality for managing Extract, Transform, and Load (ETL) processes through a Python-based application. It allows users to create or load instances of the ETL_MANAGER client, manage connections to databases, create projects, define SQL scripts within projects, and set up automations to execute scripts in a specified order on a schedule.

### Features

1. **Client Management**
   - Create or load instances of the ETL_MANAGER client protected with a password using hash/salt strategy.

2. **Connection Management**
   - Define connections to databases for accessing data sources.

3. **Project Management**
   - Create projects within clients to organize SQL scripts.

4. **Script Management**
   - Define SQL scripts within projects to perform data transformations.

5. **Automation**
   - Set up automations within projects to execute SQL scripts in a specified order on a schedule.

### Components

1. **Core Module (`core.py`):**
   - Defines classes for managing clients, connections, projects, scripts, and automations.
   - Implements functionality for password protection, saving/loading client data, executing SQL scripts, and managing automations.

2. **API Module (`app.py`):**
   - Provides endpoints for interacting with the ETL_MANAGER client through HTTP requests.
   - Endpoints allow creating/loading clients, managing connections, projects, scripts, and automations.

3. **API Wrapper (`api_wrapper.py`):**
   - Offers a Python interface to interact with the API provided by the `app.py` module.
   - Contains methods for calling API endpoints to perform various actions such as creating clients, managing connections, projects, scripts, and automations.

### Usage

1. **Setting Up Clients:**
   - Use the provided API endpoints or the API wrapper to create or load instances of the ETL_MANAGER client.
   - Clients are protected with passwords using a hash/salt strategy for security.

2. **Managing Connections:**
   - Define connections to databases by providing necessary details such as account information, connection type, username, and password.

3. **Project and Script Management:**
   - Create projects within clients to organize SQL scripts.
   - Define SQL scripts within projects to perform specific data transformations.

4. **Automation Setup:**
   - Set up automations within projects to execute SQL scripts in a specified order on a schedule.
   - Automations help automate repetitive tasks in the ETL process.

### API Documentation

- **Endpoint:** `/create_or_load_client`
  - **Method:** `POST`
  - **Parameters:**
    - `instance_name`: Name of the client instance.
    - `username`: Username for client authentication.
    - `password`: Password for client authentication.
    - `method`: Method to create/load client instance.

- **Endpoint:** `/create_connection`
  - **Method:** `POST`
  - **Parameters:**
    - `instance_name`: Name of the client instance.
    - `username`: Username for client authentication.
    - `password`: Password for client authentication.
    - `connection_name`: Name of the database connection.
    - `connection_type`: Type of database connection.
    - `account`: Account information for database connection.
    - `connection_username`: Username for database connection.
    - `connection_password`: Password for database connection.

- **Endpoint:** `/create_project`
  - **Method:** `POST`
  - **Parameters:**
    - `instance_name`: Name of the client instance.
    - `username`: Username for client authentication.
    - `password`: Password for client authentication.
    - `project_name`: Name of the project to be created.

- **Endpoint:** `/create_script`
  - **Method:** `POST`
  - **Parameters:**
    - `instance_name`: Name of the client instance.
    - `username`: Username for client authentication.
    - `password`: Password for client authentication.
    - `project_name`: Name of the project.
    - `script_name`: Name of the SQL script.
    - `script_code`: Code for the SQL script.

- **Endpoint:** `/create_automation`
  - **Method:** `POST`
  - **Parameters:**
    - `instance_name`: Name of the client instance.
    - `username`: Username for client authentication.
    - `password`: Password for client authentication.
    - `project_name`: Name of the project.
    - `automation_name`: Name of the automation.
    - `scripts`: List of SQL scripts to be included in the automation.
    - `order`: Order of execution for SQL scripts.
    - `schedule`: Schedule for the automation execution.

- **Endpoint:** `/start_automation`
  - **Method:** `POST`
  - **Parameters:**
    - `instance_name`: Name of the client instance.
    - `username`: Username for client authentication.
    - `password`: Password for client authentication.
    - `project_name`: Name of the project.
    - `automation_name`: Name of the automation to start.
    - `connection_name`: Name of the database connection to be used.

- **Endpoint:** `/stop_automation`
  - **Method:** `POST`
  - **Parameters:**
    - `instance_name`: Name of the client instance.
    - `username`: Username for client authentication.
    - `password`: Password for client authentication.
    - `project_name`: Name of the project.
    - `automation_name`: Name of the automation to stop.

### Dependencies

- Flask: Web framework for building API endpoints.
- requests: HTTP library for making requests to the API endpoints.
- snowflake-connector: Snowflake Python Connector for database connections.
- crontab: Library for managing cron jobs.

### Running the Application

1. Ensure Python and required dependencies are installed.
2. Run the Flask application by executing `app.py`.
3. Use the provided API endpoints or the API wrapper (`api_wrapper.py`) to interact with the application.

### Note

- Ensure proper authentication and authorization mechanisms are implemented in a production environment to secure access to the ETL_MANAGER application.
- Handle errors and exceptions gracefully to ensure smooth operation of the application.

### Contributors

- Jackson Makl

