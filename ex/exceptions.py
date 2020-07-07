class DemoException(Exception):
    codigo = None
    mensaje = None
    
    def __init__(self, codigo: int, mensaje: str):
        self.codigo = codigo
        self.mensaje = mensaje


class NotFound(DemoException):
    def __init__(self, mensaje):
        super().__init__(404, mensaje)

class BadRequest(DemoException):
    def __init__(self, mensaje):
        super().__init__(400, mensaje)

class InternalServerError(DemoException):
    def __init__(self, mensaje):
        super().__init__(500, mensaje)
