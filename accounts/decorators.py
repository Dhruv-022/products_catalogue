from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def role_required(allowed_roles=None):
  """Decorator that checks if an authenticated user belongs to one of the allowed roles.

  Usage:
      @role_required([User.Role.SYSTEM_ADMIN, User.Role.OWNER])
  """
  if allowed_roles is None:
    allowed_roles = []

  def decorator(view_func):

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
      # Must be authenticated first
      if not request.user.is_authenticated:
        return redirect("dashboard:login")

      # Check role membership
      if request.user.role in allowed_roles:
        return view_func(request, *args, **kwargs)

      # 403 Forbidden if not authorized
      raise PermissionDenied("You do not have permission to view this page.")

    return _wrapped_view

  return decorator


def system_admin_required(view_func):
  """Quick shorthand decorator for System Admin only."""
  from accounts.models import User

  return role_required([User.Role.SYSTEM_ADMIN])(view_func)


def owner_or_admin_required(view_func):
  """Quick shorthand decorator for Owner and System Admin."""
  from accounts.models import User

  return role_required([User.Role.SYSTEM_ADMIN, User.Role.OWNER])(view_func)