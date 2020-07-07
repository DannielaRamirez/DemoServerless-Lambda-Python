import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from ex import exceptions

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("DemoServerless")

def get_all():
	try:
		response = table.query(
			KeyConditionExpression = Key("hk").eq("EMPLEADO")
		)
		print(response)

	except ClientError as e:
		raise exceptions.InternalServerError(e.response['Error']['Message'])

	else:
		if "Items" not in response or not response["Items"]:
			raise exceptions.NotFound("No existe ningún registros")

		registros = response['Items']
		for registro in registros:
			registro["codigo"] = registro["sk"]
			del registro["hk"]
			del registro["sk"]
			del registro["busqueda"]

		return registros
