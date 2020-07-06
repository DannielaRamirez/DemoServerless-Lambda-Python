import json
import boto3
import decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

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

def get_all():
	try:
		response = table.query(
			KeyConditionExpression = Key("hk").eq("EMPLEADO")
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
				"body": json.dumps({"error": "No existe ningún registros"})
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
