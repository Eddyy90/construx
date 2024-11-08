from ninja_extra import api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

from .models import User
from .schemas import UserSchema

from ninja_extra import (
    ModelConfig,
    ModelControllerBase,
    ModelSchemaConfig,
    api_controller,
)

from ninja_extra import permissions, api_controller, http_get

class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print('>>>', request, view)
        print('>>>', permissions.SAFE_METHODS)
        print('>>> user', request.user)
        print('>>> user', request.user)

        if not request.user.is_authenticated:
            return False
        url_name = request.resolver_match.url_name

        if url_name.endswith("-create"):
            return request.user.has_perm('users.add_user')

        if url_name.endswith("-list"):
            return request.user.has_perm('users.view_user')

        if url_name.endswith("-update"):
            return request.user.has_perm('users.change_user')

        if url_name.endswith("-partial-update"):
            return request.user.has_perm('users.change_user')

        if url_name.endswith("-delete"):
            return request.user.has_perm('users.delete_user')

        return request.method in permissions.SAFE_METHODS


@api_controller("", tags=["Users"])
class UserController:

    @route.get("/users/me", auth=AsyncJWTAuth(), response={200: UserSchema})
    async def get_authenticated_user(
        self, request
    ) -> User:
        return self.context.request.auth


@api_controller("/events", auth=AsyncJWTAuth(), permissions=[permissions.IsAuthenticated & HasPermission])
class UserModelController(ModelControllerBase):
    model_config = ModelConfig(
        model=User,
        async_routes=True,
        schema_config=ModelSchemaConfig(
            read_only_fields=["id"],
            exclude=["password", "is_superuser"],
            depth=0
        ),
    )