import json
import boto3
from botocore.exceptions import ClientError
from ex import exceptions

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("DemoServerless")

def get(codigo):
	print(codigo)
	
	try:
		response = table.get_item(
			Key = {
				"hk": "EMPLEADO",
				"sk": codigo
			}
		)
		print(response)

	except ClientError as e:
		raise exceptions.InternalServerError(e.response['Error']['Message'])

	else:
		if "Item" not in response:
			raise exceptions.NotFound("No existe el código '{}'".format(codigo))

		registro = response['Item']
		registro["codigo"] = registro["sk"]
		del registro["hk"]
		del registro["sk"]
		del registro["busqueda"]
		
		return registro
