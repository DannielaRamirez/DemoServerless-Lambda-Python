import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from urllib import parse
from ex import exceptions

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("DemoServerless")

def search(query):
	print(query)
	
	tokens = str(query).lower().split("+")

	filter_expression = " and ".join(["contains(busqueda, :query{})".format(idx) for idx, valor in enumerate(tokens)])

	attribute_values = {}
	for idx, token in enumerate(tokens):
		attribute_values.update({":query{}".format(idx): token})

	try:
		response = table.query(
			KeyConditionExpression = Key("hk").eq("EMPLEADO"),
			FilterExpression = filter_expression,
			ExpressionAttributeValues = attribute_values
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
