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
