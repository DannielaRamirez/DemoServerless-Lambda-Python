import json
import decimal
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from urllib import parse

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("DemoServerless")

headers = {
	'Access-Control-Allow-Origin': '*',
	'Access-Control-Allow-Methods': '*',
	'Content-Type': 'application/json'
}

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
	print(event)
	
	query = parse.unquote(event["pathParameters"]["query"])
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
		return {
			"statusCode": 500,
			"headers": headers,
			"body": json.dumps({"error": e.response['Error']['Message']})
		}

	else:
		if "Items" not in response or not response["Items"]:
			return {
				"statusCode": 404,
				"headers": headers,
				"body": json.dumps({"error": "No hubo resultados para la búsqueda: {}".format(query)})
			}

		registros = response['Items']
		for registro in registros:
			registro["codigo"] = registro["sk"]
			del registro["hk"]
			del registro["sk"]
			del registro["busqueda"]

		return {
			"statusCode": 200,
			"headers": headers,
			"body": json.dumps(registros, cls=DecimalEncoder, ensure_ascii=False)
		}
