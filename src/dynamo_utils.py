import boto3

# Use your named profile + region explicitly
session = boto3.Session(profile_name='GreenGrid', region_name='us-east-1')
dynamodb = session.resource('dynamodb')

def get_or_create_table(table_name="EnergyUsage"):
    try:
        table = dynamodb.Table(table_name)
        table.load()
        print(f"Table '{table_name}' already exists.")
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        print(f"Creating table '{table_name}'...")
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'household_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'household_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print(f"Table '{table_name}' created.")
    return table

def save_energy_data(simulated_data, table_name="EnergyUsage"):
    table = get_or_create_table(table_name)
    with table.batch_writer() as batch:
        for item in simulated_data:
            db_item = {
                'household_id': str(item['household_id']),
                'timestamp': str(item['timestamp']),
                'energy_kWh': str(item['energy_kWh'])
            }
            try:
                batch.put_item(Item=db_item)
            except Exception as e:
                print(f"Error saving item {db_item}: {e}")
    print(f"Data saved successfully to '{table_name}'.")
