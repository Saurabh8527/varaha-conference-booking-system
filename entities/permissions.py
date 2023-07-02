from enum import Enum
 
class Permissions(Enum):
    """
    Enumeration defining the permissions for various actions in the booking system.
    Each permission is represented by a unique value.

    Permissions:
    CREATE_BUILDING: Permission to create a building.
    READ_BUILDING: Permission to read the details of a building.
    DELETE_BUILDING: Permission to delete a building.
    CREATE_FLOOR: Permission to create a floor.
    READ_FLOOR: Permission to read the details of a floor.
    DELETE_FLOOR: Permission to delete a floor.
    CREATE_ROOM: Permission to create a room.
    READ_ROOM: Permission to read the details of a room.
    DELETE_ROOM: Permission to delete a room.
    CREATE_ORGANIZATION: Permission to create an organization.
    READ_ORGANIZATION: Permission to read the details of an organization.
    DELETE_ORGANIZATION: Permission to delete an organization.
    CREATE_USER: Permission to create a user.
    READ_USER: Permission to read the details of a user.
    DELETE_USER: Permission to delete a user.
    CREATE_BOOKING: Permission to create a booking.
    READ_BOOKING: Permission to read the details of a booking.
    DELETE_BOOKING: Permission to delete a booking.
    """
    CREATE_BUILDING = 1
    READ_BUILDING = 2
    DELETE_BUILDING = 3
    CREATE_FLOOR = 4
    READ_FLOOR = 5
    DELETE_FLOOR = 6
    CREATE_ROOM = 7
    READ_ROOM = 8
    DELETE_ROOM = 9
    CREATE_ORGANIZATION = 10
    READ_ORGANIZATION = 11
    DELETE_ORGANIZATION = 12
    CREATE_USER = 13
    READ_USER = 14
    DELETE_USER = 15
    CREATE_BOOKING = 16
    READ_BOOKING = 17
    DELETE_BOOKING = 18

