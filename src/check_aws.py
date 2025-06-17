import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def main():
    try:
        sts_client = boto3.client('sts')
        identity = sts_client.get_caller_identity()
        print("AWS credentials are valid.")
        print(f"Account: {identity['Account']}")
        print(f"UserId: {identity['UserId']}")
        print(f"ARN: {identity['Arn']}")
    except NoCredentialsError:
        print("No AWS credentials found. Please configure your AWS credentials.")
    except ClientError as e:
        print(f"AWS Client Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
