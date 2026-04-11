from django.db import migrations

def create_permissions_and_roles(apps, schema_editor):
    Permission = apps.get_model('accounts', 'Permission')
    Role = apps.get_model('accounts', 'Role')

    # Define all permissions
    permissions = [
        ('manage_users', 'Can manage users (create, edit, delete)'),
        ('manage_rooms', 'Can manage rooms'),
        ('manage_bookings', 'Can manage bookings'),
        ('manage_customers', 'Can manage customers'),
        ('view_reports', 'Can view reports'),
        # Add more as needed
    ]

    for code, name in permissions:
        Permission.objects.get_or_create(code=code, name=name)

    # Create roles with permissions
    admin_role, _ = Role.objects.get_or_create(name='Admin')
    admin_role.permissions.set(Permission.objects.all())

    manager_role, _ = Role.objects.get_or_create(name='Manager')
    manager_perms = ['manage_rooms', 'manage_bookings', 'manage_customers', 'view_reports']
    manager_role.permissions.set(Permission.objects.filter(code__in=manager_perms))

    receptionist_role, _ = Role.objects.get_or_create(name='Receptionist')
    receptionist_perms = ['manage_bookings', 'manage_customers']
    receptionist_role.permissions.set(Permission.objects.filter(code__in=receptionist_perms))

    housekeeping_role, _ = Role.objects.get_or_create(name='Housekeeping')
    housekeeping_perms = ['manage_rooms']   # only room status updates
    housekeeping_role.permissions.set(Permission.objects.filter(code__in=housekeeping_perms))

    accountant_role, _ = Role.objects.get_or_create(name='Accountant')
    accountant_perms = ['view_reports']
    accountant_role.permissions.set(Permission.objects.filter(code__in=accountant_perms))

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_permissions_and_roles, reverse_func),
    ]