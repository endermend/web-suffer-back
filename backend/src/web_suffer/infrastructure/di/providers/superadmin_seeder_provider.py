from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from web_suffer.infrastructure.seeders.superadmin_seeder import SuperAdminSeeder


class SuperAdminSeederProvider(Provider):
    """Провайдер для SuperAdminSeeder."""

    scope = Scope.REQUEST

    super_admin_seeder = provide(SuperAdminSeeder)
