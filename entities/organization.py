import threading
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

from utils import get_monthly_hours
import constants


class Organization:
    """
    Represents an organization with employees and bookings.
    """
    def __init__(self, name, email, phone):
        """
        Initializes a new instance of the Organization class.

        Args:
            name (str): The name of the organization.
            email (str): The email address of the organization.
            phone (str): The phone number of the organization.
        """
        self.lock = threading.Lock()
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        # all employees of this organization
        self.employee_ids = []
        # all bookings made by this organization
        self.booking_ids = []
        # (month, year) to hours mapping...
        self.booked_hours = defaultdict(int)

    def add_employees(self, employee_ids):
        """
        Retrieves all the bookings made by the organization.

        Returns:
            list: A list of booking objects made by the organization.

        Note:
            This method is thread-safe due to the use of a lock.
        """
        with self.lock:
            self.employees.extend(employee_ids)

    def add_booking(self, room, employee, booking):
        """
        Adds a booking for a room made by an employee in the organization.

        Args:
            room (Room): The room object to book.
            employee (Employee): The employee object making the booking.
            booking (Booking): The booking object to add.

        Returns:
            bool: True if the booking was added successfully, False otherwise.

        Raises:
            Exception: If the booking duration exceeds the maximum allowed duration or the monthly booking hour limit is exceeded.
        """
        with self.lock:
            booking_duration = (
                booking.end_time - booking.start_time).total_seconds() // constants.SECONDS_IN_HOUR
            if booking_duration >= constants.BOOKING_MAX_DURATION:
                raise Exception("booking 1 slot greater than {} hours not allowed".format(
                    constants.BOOKING_MAX_DURATION))

            monthly_hours = get_monthly_hours(
                booking.start_time, booking.end_time)
            for month in monthly_hours:
                if self.booked_hours[month] + monthly_hours[month] > constants.MONTHLY_BOOKING_HOUR_LIMIT:
                    raise Exception("cannot book for more than {} hours in a month".format(
                        constants.MONTHLY_BOOKING_HOUR_LIMIT))

            room.add_booking(booking)
            employee.add_booking(booking)

            self.booking_ids.append(booking.id)
            for month in monthly_hours:
                self.booked_hours[month] += monthly_hours[month]

            return True

    def remove_booking(self, room, employee, booking):
        """
        Removes a booking made by an employee for a room from the organization.

        Args:
            room (Room): The room object for which the booking was made.
            employee (Employee): The employee who made the booking.
            booking (Booking): The booking object to remove.

        Returns:
            bool: True if the booking was removed successfully, False otherwise.
        """
        with self.lock:
            room.remove_booking(booking)
            employee.remove_booking(booking)

            monthly_hours = get_monthly_hours(
                booking.start_time, booking.end_time)
            for month in monthly_hours:
                self.booked_hours[month] -= monthly_hours[month]

            return True

    def __repr__(self):
        """
        Returns a string representation of the Organization object.

        Returns:
            str: A string representation of the Organization object.
        """
        return str({"id": self.id, "name": self.name, "email": self.email, "phone": self.phone, "employee_ids": self.employee_ids, "booking_ids": self.booking_ids, "booked_hours": self.booked_hours})
