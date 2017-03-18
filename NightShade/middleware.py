from django.conf import settings
from tenant_schemas.middleware import DefaultTenantMiddleware

class SettingTenantMiddleware(DefaultTenantMiddleware):
    DEFAULT_SCHEMA_NAME = settings.SCHEMA_DEFAULT
