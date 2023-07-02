from datetime import datetime, timedelta
from collections import defaultdict

from entities.permissions import Permissions
import constants

def user_has_permission(user, required_permission):
    """
    Checks if a user has a specific permission.

    Args:
        user (User): The user object to check.
        required_permission (Permissions): The required permission.

    Returns:
        bool: True if the user has the required permission, False otherwise.
    """
    for role in user.roles:
        for permission in role.permissions:
            if Permissions(permission) == required_permission:
                return True

    return False


def check_user_permissions(required_permission):
    """
    Decorator to check if a user has a specific permission before executing a method.

    Args:
        required_permission (Permissions): The required permission.

    Returns:
        function: The decorator function.

    Note:
        This decorator assumes the presence of a `users` attribute in the decorated class.
        The `users` attribute is expected to be a dictionary with user IDs as keys and user objects as values.
    """
    def decorator(func):
        def wrapper(self, caller_id, *args, **kwargs):
            user = self.users.get(caller_id)
            if not user:
                raise Exception("User not found!")
            if user_has_permission(user, required_permission):
                return func(self, caller_id, *args, **kwargs)
            else:
                raise Exception("User: {} does not have the required permission to {}".format(user.name, required_permission.name))
        return wrapper
    return decorator


def get_day_wise_slots(start, end):
    """
    Divides a time range into day-wise slots.

    Args:
        start (datetime): The start time of the range.
        end (datetime): The end time of the range.

    Returns:
        dict: A dictionary where the keys are the dates and the values are the time slots for each date.
    """
    day_delta = timedelta(days = 1)
    start_date = datetime(start.year, start.month, start.day)
    end_date = datetime(end.year, end.month, end.day)
    if start_date == end_date:
        return {start_date: (start, end)}

    day_slots = {}
    curr = start_date
    while(curr <= end_date):
        time_slot = (curr, curr + day_delta)
        if curr == start_date:
            time_slot = (start, curr + day_delta)
        elif curr == end_date:
            time_slot = (curr, end)
        day_slots[curr] = time_slot
        curr += day_delta

    return day_slots


def slots_overlapping(time_slot1, time_slot2):
    """
    Checks if two time slots overlap.

    Args:
        time_slot1 (tuple): The first time slot as a tuple of start and end times.
        time_slot2 (tuple): The second time slot as a tuple of start and end times.

    Returns:
        bool: True if the time slots overlap, False otherwise.
    """
    slot1_start, slot1_end = time_slot1
    slot2_start, slot2_end = time_slot2
    if slot1_start < slot2_end and slot2_start < slot1_end:
        return True
    return False


def check_overlapping(time_slots, time_slot):
    """
    Checks if a time slot overlaps with any of the existing time slots.

    Args:
        time_slots (list): A list of existing time slots.
        time_slot (tuple): The time slot to check.

    Returns:
        bool: True if the time slot overlaps with any of the existing time slots, False otherwise.
    """
    for slot in time_slots:
        if slots_overlapping(slot, time_slot):
            return True

    return False


def get_monthly_hours(start_time, end_time):
    """
    Calculates the number of hours booked per month within a given time range.

    Args:
        start_time (datetime): The start time of the booking range.
        end_time (datetime): The end time of the booking range.

    Returns:
        defaultdict: A dictionary with (month, year) tuples as keys and the corresponding hours as values.
    """
    monthly_hours = defaultdict(int)
    start_month, start_year = start_time.month, start_time.year
    end_month, end_year = end_time.month, end_time.year
    hours_in_start_month, hours_in_end_month = 0, 0
    if start_month != end_month:
        end_month_start_time = datetime(end_year, end_month, day=1)
        hours_in_start_month = (end_month_start_time - start_time).total_seconds() // constants.SECONDS_IN_HOUR
        hours_in_end_month = (end_time - end_month_start_time).total_seconds() // constants.SECONDS_IN_HOUR

    if start_month != end_month:
        monthly_hours[(start_month, start_year)] += hours_in_start_month
        monthly_hours[(end_month, end_year)] += hours_in_end_month
    else:
        monthly_hours[(start_month, start_year)] += (end_time- start_time).total_seconds() // constants.SECONDS_IN_HOUR

    return monthly_hours

