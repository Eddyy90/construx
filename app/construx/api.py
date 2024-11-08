from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from users.api import UserModelController
from animals.api import AnimalModelController
from vets.api import VetModelController


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(UserModelController)
api.register_controllers(AnimalModelController)
api.register_controllers(VetModelController)


@api.get("/ping")
def ping(request):
    return "pong"
