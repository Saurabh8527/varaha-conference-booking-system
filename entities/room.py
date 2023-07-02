import threading
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from utils import get_day_wise_slots, check_overlapping


class Room:
    """
    Represents a room in a building.
    """
    def __init__(self, building_id, floor_id, name, number, capacity, equipments=set()):
        """
        Initializes a new instance of the Room class.

        Args:
            building_id (str): The ID of the building the room belongs to.
            floor_id (str): The ID of the floor the room is located on.
            name (str): The name of the room.
            number (int): The number of the room.
            capacity (int): The maximum capacity of the room.
            equipments (set, optional): The set of equipments available in the room. Defaults to an empty set.
        """
        self.lock = threading.Lock()
        self.id = str(uuid.uuid4())
        self.building_id = building_id
        self.floor_id = floor_id
        self.name = name
        self.number = number
        self.capacity = capacity
        self.equipments = equipments
        self.booking_ids = []
        self.booked_timings = defaultdict(list)

    def add_equipment(self, equipment):
        """
        Adds an equipment to the room.

        Args:
            equipment (str): The equipment to add to the room.
        """
        with self.lock:
            self.available_equipments.add(equipment)

    def remove_equipment(self, equipment):
        """
        Removes an equipment from the room.

        Args:
            equipment (str): The equipment to remove from the room.
        """
        with self.lock:
            self.available_equipments.remove(equipment)

    def add_booking(self, booking):
        """
        Adds a booking to the room.

        Args:
            booking (Booking): The booking object to add.

        Returns:
            bool: True if the booking was added successfully, False otherwise.

        Raises:
            Exception: If the room is already booked for somepart  of the time slot.
        """
        with self.lock:
            day_slots = get_day_wise_slots(
                booking.start_time, booking.end_time)
            if any([check_overlapping(self.booked_timings[day], day_slots[day]) for day in day_slots]):
                raise Exception(
                    "Room is already booked for some part of the time slot!")

            self.booking_ids.append(booking.id)
            for day in day_slots:
                self.booked_timings[day].append(day_slots[day])
            return True

    def remove_booking(self, booking_to_be_removed):
        """
        Removes a booking from the room.

        Args:
            booking_to_be_removed (Booking): The booking object to be removed.

        Returns:
            bool: True if the booking was removed successfully, False otherwise.
        """
        with self.lock:
            day_slots = get_day_wise_slots(
                booking_to_be_removed.start_time, booking_to_be_removed.end_time)
            for day in day_slots:
                for slot in self.booked_timings[day]:
                    if slot == day_slots[day]:
                        self.booked_timings[day].remove(slot)

            self.booking_ids.remove(booking_to_be_removed.id)
            return True

    def __repr__(self):
        """
        Returns a string representation of the Room object.

        Returns:
            str: A string representation of the Room object.
        """
        return str({"id": self.id, "building_id": self.building_id, "floor_id": self.floor_id, "name": self.name, "number": self.number, "capacity": self.capacity, "equipments": self.equipments, "booking_ids": self.booking_ids, "booked_timings": self.booked_timings})
