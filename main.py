from api_wraper import ClientAPI


if __name__ == '__main__':
    client_wrapper = ClientAPI()

    # Example usage of API endpoints
    result = client_wrapper.create_or_load_client('DEMO', 'ADMIN', 'PASSWORD', 'create')
    print(result)

    result = client_wrapper.create_connection('DEMO', 'ADMIN', 'PASSWORD', 'Snowflake', 'SNOWFLAKE', '*******',
                                              '******', '******')
    print(result)

    result = client_wrapper.create_project('DEMO', 'ADMIN', 'PASSWORD', 'test_project')
    print(result)

    result = client_wrapper.create_script('DEMO', 'ADMIN', 'PASSWORD', 'test_project', 'test_script.sql', 'select 1;')
    print(result)

    result = client_wrapper.create_automation('DEMO', 'ADMIN', 'PASSWORD', 'test_project', 'daily', ['test_script.sql'],
                                              ['test_script.sql'], 5)
    print(result)

    result = client_wrapper.start_automation('DEMO', 'ADMIN', 'PASSWORD', 'test_project', 'daily', 'Snowflake')
    print(result)

    result = client_wrapper.stop_automation('DEMO', 'ADMIN', 'PASSWORD', 'test_project', 'daily')
    print(result)