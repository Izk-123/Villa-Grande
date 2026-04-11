def has_permission(user, perm_code):
    """Return True if the user has the given permission."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if not hasattr(user, 'profile') or not user.profile.role:
        return False
    return user.profile.role.permissions.filter(code=perm_code).exists()