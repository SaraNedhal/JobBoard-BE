from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
      
class UserTypePermission(BasePermission):
    """
    Custom permission to restrict access based on user type.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Extract user type from the user object
            user_type = request.user.profile.role  # Assuming you have a 'user_type' field in your User model

            # Define the allowed user types for the view
            allowed_user_types = getattr(view, 'allowed_user_types', [])

            # Check if the user type is in the allowed user types
            return user_type in allowed_user_types

        # If the user is not authenticated, deny access
        return False
