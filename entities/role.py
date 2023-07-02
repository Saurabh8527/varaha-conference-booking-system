
class Role:
    """
    Represents a role within the booking system with associated permissions.
    """
    def __init__(self, name, permissions=[]):
        """
        Initialize a new Role object.

        Args:
            name (str): The name of the role.
            permissions (list[Permissions], optional): List of permissions associated with the role. Defaults to an empty list.
        """
        self.name = name
        self.permissions = permissions

    def update_permissions(self, new_permissions):
        """
        Update the permissions of the role.

        Args:
            new_permissions (list[Permissions]): New list of permissions to be associated with the role.
        """
        self.permissions = new_permissions
