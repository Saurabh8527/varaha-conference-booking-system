from entities.permissions import Permissions
from entities.building import Building
from entities.floor import Floor
from entities.room import Room
from entities.organization import Organization
from entities.user import User
from entities.booking import Booking
from utils import check_user_permissions


class BookingSystem:
    """
    Represents a booking system
    """
    def __init__(self, super_admin_user):
        self.super_admin_user = super_admin_user
        self.buildings = {}
        self.floors = {}
        self.rooms = {}
        self.bookings = {}
        self.organizations = {}
        self.users = {super_admin_user.id: super_admin_user}

    @check_user_permissions(Permissions.CREATE_BUILDING)
    def add_building(self, caller_id, name):
        new_building = Building(name)
        while (new_building.id in self.buildings):
            new_building = Building(name)

        self.buildings[new_building.id] = new_building
        return new_building

    @check_user_permissions(Permissions.READ_BUILDING)
    def get_building(self, caller_id, id):
        return self.buildings.get(id)

    @check_user_permissions(Permissions.CREATE_FLOOR)
    def add_floor(self, caller_id, building_id, number):
        building = self.buildings[building_id]
        if not building:
            raise Exception("building not found!")
        new_floor = Floor(building_id, number)
        while (new_floor.id in self.floors):
            new_floor = Floor(building_id, number)

        building.add_floors([new_floor.id])
        self.floors[new_floor.id] = new_floor
        return new_floor

    @check_user_permissions(Permissions.READ_FLOOR)
    def get_floor(self, caller_id, id):
        return self.floors.get(id)

    @check_user_permissions(Permissions.CREATE_ROOM)
    def add_room(self, caller_id, building_id, floor_id, name, number, capacity, equipments):
        building = self.buildings.get(building_id)
        if not building:
            raise Exception("building not found!")
        floor = self.floors.get(floor_id)
        if not floor:
            raise Exception("floor not found!")
        new_room = Room(building_id, floor_id, name,
                        number, capacity, equipments)
        while (new_room.id in self.rooms):
            new_room = Room(building_id, floor_id, name,
                            number, capacity, equipments)

        floor.add_rooms([new_room.id])
        self.rooms[new_room.id] = new_room
        return new_room

    @check_user_permissions(Permissions.READ_ROOM)
    def get_room(self, caller_id, id):
        return self.rooms.get(id)

    @check_user_permissions(Permissions.CREATE_ORGANIZATION)
    def add_organization(self, caller_id, name, email, phone):
        new_organization = Organization(name, email, phone)
        while (new_organization.id in self.organizations):
            new_organization = Organization(name, email, phone)

        self.organizations[new_organization.id] = new_organization
        return new_organization

    @check_user_permissions(Permissions.READ_ORGANIZATION)
    def get_organization(self, caller_id, id):
        return self.organizations.get(id)

    @check_user_permissions(Permissions.CREATE_USER)
    def add_user(self, caller_id, organization_id, name, email, phone, roles):
        user = self.users.get(caller_id)
        if not user == self.super_admin_user and user.organization_id != organization_id:
            raise Exception(
                "user: {} does not belong to this organization!".format(user.name))

        organization = self.organizations.get(organization_id)
        if not organization:
            raise Exception("organization not found!")

        new_user = User(organization_id, name, email, phone, roles)
        while (new_user.id in self.users):
            new_user = User(organization_id, name, email, phone, roles)

        self.users[new_user.id] = new_user
        return new_user

    @check_user_permissions(Permissions.READ_USER)
    def get_user(self, caller_id, id):
        return self.users.get(id)

    @check_user_permissions(Permissions.READ_ROOM)
    def find_rooms(self, caller_id, building_id, start_time=None, end_time=None, floor_number=-1, capacity=-1, required_equipments={}):
        building = self.buildings.get(building_id)
        if not building:
            raise Exception("building not found!")

        floors = [self.floors[floor_id] for floor_id in building.floor_ids if (
            floor_number == -1 or self.floors[floor_id].number == floor_number)]
        rooms = [self.rooms[room_id] for floor in floors for room_id in floor.room_ids if self.rooms[room_id].capacity >=
                 capacity and all([equipment in self.rooms[room_id].equipments for equipment in required_equipments])]

        formatted_rooms = [{
            "id": room.id,
            "name": room.name,
            "room_number": room.number,
            "capacity": room.capacity,
            "floor_number": self.floors[room.floor_id].number,
            "booked_timings": {day: room.booked_timings[day] for day in room.booked_timings}
        } for room in rooms]
        return formatted_rooms

    @check_user_permissions(Permissions.CREATE_BOOKING)
    def book_room(self, caller_id, organization_id, name, room_id, start_time, end_time):
        user = self.users.get(caller_id)
        if not user == self.super_admin_user and user.organization_id != organization_id:
            raise Exception(
                "user: {} does not belong to this organization!".format(user.name))

        organization = self.organizations.get(organization_id)
        if not organization:
            raise Exception("organization not found!")

        room = self.rooms.get(room_id)
        if not room:
            raise Exception("room not found!")

        if start_time.minute != 0 or start_time.second != 0 or end_time.minute != 0 or end_time.second != 0:
            raise Exception("can only book hourly meet")

        new_booking = Booking(name, start_time, end_time,
                              room_id, organization_id, user_id=caller_id)
        organization.add_booking(room, user, new_booking)
        self.bookings[new_booking.id] = new_booking
        print("room: {} booked for user: {}".format(room.name, user.name))
        return new_booking

    @check_user_permissions(Permissions.DELETE_BOOKING)
    def cancel_booking(self, caller_id, booking_id):
        booking = self.bookings.get(booking_id)
        if not booking:
            raise Exception("booking not found!")

        user = self.users[caller_id]
        if not user == self.super_admin_user and user.organization_id != booking.organization_id:
            raise Exception(
                "user: {} does not belong to this organization!".format(user.name))

        organization = self.organizations[booking.organization_id]
        room = self.rooms[booking.room_id]
        organization.remove_booking(room, user, booking)
        print("booking for room: {} cancelled for user: {}".format(room.name, user.name))
        return True

    @check_user_permissions(Permissions.READ_BOOKING)
    def get_user_bookings(self, caller_id):
        user = self.users[caller_id]
        user_bookings = [self.bookings[id] for id in user.booking_ids]
        user_bookings.sort(key=lambda booking: booking.start_time)

        formatted_bookings = [{
            "id": booking.id,
            "name": booking.name,
            "start_time": booking.start_time.isoformat(),
            "end_time": booking.end_time.isoformat(),
            "organization_name": self.organizations[booking.organization_id].name,
            "user_name": user.name
        } for booking in user_bookings]

        return formatted_bookings

    @check_user_permissions(Permissions.READ_BOOKING)
    def get_organization_bookings(self, caller_id, organization_id):
        user = self.users[caller_id]
        if not user == self.super_admin_user and user.organization_id != organization_id:
            raise Exception(
                "user: {} does not belong to this organization!".format(user.name))

        organization = self.organizations[organization_id]
        if not organization:
            raise Exception("organization not found!")

        organization_bookings = [self.bookings[id]
                                 for id in organization.booking_ids]
        organization_bookings.sort(key=lambda booking: booking.start_time)

        formatted_bookings = [{
            "id": booking.id,
            "name": booking.name,
            "start_time": booking.start_time.isoformat(),
            "end_time": booking.end_time.isoformat(),
            "organization_name": self.organizations[booking.organization_id].name,
            "user_name": self.users[booking.user_id].name
        } for booking in organization_bookings]

        return formatted_bookings
