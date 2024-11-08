from ninja_extra import api_controller
from ninja_jwt.authentication import AsyncJWTAuth
from .models import Payment
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
            return request.user.has_perm('payments.add_payment')

        if url_name.endswith("-list"):
            return request.user.has_perm('payments.view_payment')

        if url_name.endswith("-update"):
            return request.user.has_perm('payments.change_payment')

        if url_name.endswith("-partial-update"):
            return request.user.has_perm('payments.change_payment')

        if url_name.endswith("-delete"):
            return request.user.has_perm('payments.delete_payment')

        return request.method in permissions.SAFE_METHODS


@api_controller("/payments", auth=AsyncJWTAuth(), permissions=[permissions.IsAuthenticated & HasPermission])
class PaymentModelController(ModelControllerBase):
    model_config = ModelConfig(
        model=Payment,
        async_routes=True,
        schema_config=ModelSchemaConfig(
            read_only_fields=["id"],
            exclude=["password", "is_superuser"],
            depth=0
        ),
    )