import uuid


class Booking:
    """
    Represents a booking for a room.
    """
    def __init__(self, name, start_time, end_time, room_id, organization_id, user_id):
        """
        Initializes a new instance of the Booking class.

        Args:
            name (str): The name of the booking.
            start_time (datetime): The start time of the booking.
            end_time (datetime): The end time of the booking.
            room_id (str): The ID of the room being booked.
            organization_id (str): The ID of the organization making the booking.
            user_id (str): The ID of the user making the booking.
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.room_id = room_id
        self.organization_id = organization_id
        self.user_id = user_id

    def __repr__(self):
        """
        Returns a string representation of the Booking object.

        Returns:
            str: A string representation of the Booking object.
        """
        return str({"id": self.id, "name": self.name, "start_time": self.start_time, "end_time": self.end_time, "room_id": self.room_id, "organization_id": self.organization_id, "user_id": self.user_id})
