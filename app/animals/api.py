from ninja_extra import api_controller
from ninja_jwt.authentication import AsyncJWTAuth
from .models import Animal
from ninja_extra import permissions, api_controller
from ninja_extra import (
    ModelConfig,
    ModelControllerBase,
    ModelSchemaConfig,
    api_controller,
)

class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        url_name = request.resolver_match.url_name

        if url_name.endswith("-create"):
            return request.user.has_perm('animals.add_animal')

        if url_name.endswith("-list"):
            return request.user.has_perm('animals.view_animal')

        if url_name.endswith("-update"):
            return request.user.has_perm('animals.change_animal')

        if url_name.endswith("-partial-update"):
            return request.user.has_perm('animals.change_animal')

        if url_name.endswith("-delete"):
            return request.user.has_perm('animals.delete_animal')

        return request.method in permissions.SAFE_METHODS


@api_controller("/animals", auth=AsyncJWTAuth(), permissions=[permissions.IsAuthenticated & HasPermission])
class AnimalModelController(ModelControllerBase):
    model_config = ModelConfig(
        model=Animal,
        async_routes=True,
        schema_config=ModelSchemaConfig(
            read_only_fields=["id"],
            exclude=["password", "is_superuser"],
            depth=0
        ),
    )