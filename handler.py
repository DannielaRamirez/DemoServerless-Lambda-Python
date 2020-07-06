import json
from urllib import parse
from api import get
from api import getAll
from api import search

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
	
	path_parameters = event["pathParameters"]
	print(path_parameters)

	if not path_parameters:
		return getAll.get_all()
	elif "codigo" in path_parameters:
		return get.get(path_parameters["codigo"])
	elif "query" in path_parameters:
		return search.search(parse.unquote(path_parameters["query"]))
	else:
		return {
			"statusCode": 400,
			"headers": headers,
			"body": json.dumps({"error": "Ruta no soportada: {}".format(path_parameters)})
	}


event = {
    "pathParameters": {}
}

lambda_handler(event, None)
