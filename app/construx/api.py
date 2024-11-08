from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from users.api import UserModelController


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(UserModelController)


@api.get("/ping")
def ping(request):
    return "pong"
