import boto3


def get_secret(name, region=None):
    client = boto3.client("secretsmanager", region_name=region or None)
    return client.get_secret_value(SecretId=name)["SecretString"]
