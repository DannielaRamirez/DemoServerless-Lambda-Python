import json
import decimal
import boto3
from botocore.exceptions import ClientError

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
		return {
			"statusCode": 500,
			"headers": headers,
			"body": json.dumps({"error": e.response['Error']['Message']})
		}

	else:
		if "Item" not in response:
			return {
				"statusCode": 404,
				"headers": headers,
				"body": json.dumps({"error": "No existe el código '{}'".format(codigo)})
			}

		registro = response['Item']
		registro["codigo"] = registro["sk"]
		del registro["hk"]
		del registro["sk"]
		del registro["busqueda"]
		
		return {
			"statusCode": 200,
			"headers": headers,
			"body": json.dumps(registro, cls=DecimalEncoder, ensure_ascii=False)
		}
