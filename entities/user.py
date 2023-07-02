import threading
import uuid


class User:
    """
    Represents a user associated with an organization.
    """
    def __init__(self, organization_id, name, email, phone, roles):
        """
        Initializes a new instance of the User class.

        Args:
            organization_id (str): The ID of the organization to which the user belongs.
            name (str): The name of the user.
            email (str): The email address of the user.
            phone (str): The phone number of the user.
            roles (list): The roles assigned to the user.
        """
        self.lock = threading.Lock()
        self.id = str(uuid.uuid4())
        self.organization_id = organization_id
        self.name = name
        self.email = email
        self.phone = phone
        # all bookings made by this user
        self.booking_ids = []
        self.roles = roles

    def add_booking(self, booking):
        """
        Adds a booking made by the user.

        Args:
            booking (Booking): The booking object to add.

        Returns:
            bool: True if the booking was added successfully, False otherwise.

        Note:
            This method is thread-safe due to the use of a lock.
        """
        with self.lock:
            self.booking_ids.append(booking.id)
            return True

    def remove_booking(self, booking):
        """
        Removes a booking made by the user.

        Args:
            booking (Booking): The booking object to remove.

        Returns:
            bool: True if the booking was removed successfully, False otherwise.

        Note:
            This method is thread-safe due to the use of a lock.
        """
        with self.lock:
            self.booking_ids.remove(booking.id)
            return True


    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return str({"id": self.id, "organization_id": self.organization_id, "name": self.name, "email": self.email, "phone": self.phone, "booking_ids": self.booking_ids, "roles": self.roles})
