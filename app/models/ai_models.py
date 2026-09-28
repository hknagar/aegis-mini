from pydantic import BaseModel


class AegisOperation(BaseModel):
    operation: str

class AegisRoute(BaseModel):

    route: str