import uuid
import threading

class Building:
    """
    Represents a building containing multiple floors and rooms.
    """
    def __init__(self, name):
        """
        Initializes a new instance of the Building class.

        Args:
            name (str): The name of the building.
        """
        self.id = str(uuid.uuid4())
        self.lock = threading.Lock()
        self.name = name
        self.floor_ids = []

    def add_floors(self, floor_ids):
        """
        Adds a list of floor IDs to the building.

        Args:
            floor_ids (list): A list of floor IDs to add to the building.

        Note:
            This method is thread-safe due to the use of a lock.
        """
        with self.lock:
            self.floor_ids.extend(floor_ids)
