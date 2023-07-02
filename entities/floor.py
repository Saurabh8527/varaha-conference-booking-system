import uuid
import threading


class Floor:
    """
    Represents a floor in a building.
    """
    def __init__(self, building_id, number):
        """
        Initializes a new instance of the Floor class.

        Args:
            building_id (str): The ID of the building the floor belongs to.
            number (int): The number of the floor.
        """
        self.id = str(uuid.uuid4())
        self.lock = threading.Lock()
        self.building_id = building_id
        self.number = number
        self.room_ids = []

    def add_rooms(self, room_ids):
        """
        Adds room IDs to the floor.

        Args:
            room_ids (list): A list of room IDs to add.

        Note:
            This method is thread-safe due to the use of a lock.
        """
        with self.lock:
            self.room_ids.extend(room_ids)

    def __repr__(self):
        """
        Returns a string representation of the Floor object.

        Returns:
            str: A string representation of the Floor object.
        """
        return str({"id": self.id, "building_id": self.building_id, "number": self.number, "room_ids": self.room_ids})
