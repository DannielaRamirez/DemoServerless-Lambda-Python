import json
import decimal
from urllib import parse
from api import get
from api import getAll
from api import search
from ex import exceptions

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

	response = None
	try:
		if not path_parameters:
			response = getAll.get_all()
		elif "codigo" in path_parameters:
			response = get.get(path_parameters["codigo"])
		elif "query" in path_parameters:
			response = search.search(parse.unquote(path_parameters["query"]))
		else:
			raise exceptions.BadRequest("Ruta no soportada: {}".format(path_parameters))

		return {
			"statusCode": 200,
			"headers": headers,
			"body": json.dumps(response, cls=DecimalEncoder, ensure_ascii=False)
		}

	except (exceptions.NotFound, exceptions.InternalServerError) as e:
		return {
			"statusCode": e.codigo,
			"headers": headers,
			"body": json.dumps({"error": e.mensaje})
		}

	except Exception as e:
		return {
			"statusCode": 500,
			"headers": headers,
			"body": json.dumps({"error": str(e)})
		}
