from datetime import datetime, timedelta

from entities.booking_system import BookingSystem
from entities.role import Role
from entities.user import User

super_admin_role = Role("super_admin", [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
org_admin_role = Role("org_admin", [2,5,8,11,13,14,15,16,17,18])
org_default_role = Role("org_user", [2,5,8,11,14,16,17,18])

super_admin_user = User(0, "super_admin_user", "super_admin@booking.com", "100", [super_admin_role])

booking_system = BookingSystem(super_admin_user)

org1 = booking_system.add_organization(super_admin_user.id, "org1", "contact@org1.com", "org1phone")
org1_admin_user = booking_system.add_user(super_admin_user.id, org1.id, "org1_admin_user", "admin@org1.com", "101", [org_admin_role])
org1_default_user = booking_system.add_user(org1_admin_user.id, org1.id, "org1_default_user", "default1@org1.com", "102", [org_default_role])

# creating building
building_1 = booking_system.add_building(super_admin_user.id, "Building 1")
try:
    # this user cannot create buildings
    building_2 = booking_system.add_building(org1_admin_user.id, "Building 2")
except Exception as err:
    print(err)

# creating floors
floor_0 = booking_system.add_floor(super_admin_user.id, building_1.id, 0)
floor_1 = booking_system.add_floor(super_admin_user.id, building_1.id, 1)
floor_2 = booking_system.add_floor(super_admin_user.id, building_1.id, 2)
try:
    # this user cannot create floors
    floor_3 = booking_system.add_floor(org1_admin_user.id, building_1.id, 3)
except Exception as err:
    print(err)

# creating rooms
room_1 = booking_system.add_room(super_admin_user.id, building_1.id, floor_0.id, "Room 1", 1, 10, {"monitor", "projector", "ac"})
room_2 = booking_system.add_room(super_admin_user.id, building_1.id, floor_0.id, "Room 2", 2, 5, {"projector"})
room_3 = booking_system.add_room(super_admin_user.id, building_1.id, floor_1.id, "Room 3", 3, 8, {})
room_4 = booking_system.add_room(super_admin_user.id, building_1.id, floor_1.id, "Room 4", 4, 10, {})
room_5 = booking_system.add_room(super_admin_user.id, building_1.id, floor_1.id, "Room 5", 5, 6, {})
room_6 = booking_system.add_room(super_admin_user.id, building_1.id, floor_2.id, "Room 6", 6, 15, {"monitor", "projector", "ac"})
try:
    # this user cannot create rooms
    room_7 = booking_system.add_room(org1_admin_user.id, building_1.id, floor_2.id, "Room 7", 7, 20, set())
except Exception as err:
    print(err)

org2 = booking_system.add_organization(super_admin_user.id, "org2", "contact@org2.com", "org2phone")
org2_admin_user = booking_system.add_user(super_admin_user.id, org2.id, "admin1_org2", "admin1@org2.com", "103", [org_admin_role])
org2_default_user = booking_system.add_user(super_admin_user.id, org2.id, "default1_org2", "default1@org2.com", "104", [org_default_role])
try:
    # the user cannot create a user for org1(org admin can only create users within their org)
    org2_default_user_2 = booking_system.add_user(org2_admin_user.id, org1.id, "default1_org2", "default1@org2.com", "105", [org_default_role])
except Exception as err:
    print(err)
try:
    # this user cannot create users
    org2_admin_user_2 = booking_system.add_user(org2_default_user.id, org2.id, "org2_admin_user_2", "admin2@org2.com", "106", [org_admin_role])
except Exception as err:
    print(err)

booking1 = booking_system.book_room(org1_default_user.id, org1.id, "Meet 1", room_1.id, datetime(2023, 7, 1, 5, 0), datetime(2023, 7, 1, 7, 0))
booking2 = booking_system.book_room(org2_default_user.id, org2.id, "Meet 2", room_1.id, datetime(2023, 7, 2, 5, 0), datetime(2023, 7, 2, 15, 0))
booking3 = booking_system.book_room(org2_default_user.id, org2.id, "Meet 3", room_2.id, datetime(2023, 7, 3, 5, 0), datetime(2023, 7, 3, 15, 0))
booking4 = booking_system.book_room(org2_default_user.id, org2.id, "Meet 4", room_5.id, datetime(2023, 7, 4, 5, 0), datetime(2023, 7, 4, 15, 0))
try:
    # booking hours exceed 30 for this month
    booking5 = booking_system.book_room(org2_default_user.id, org2.id, "Meet 5", room_1.id, datetime(2023, 7, 6, 12, 0), datetime(2023, 7, 6, 13, 0))
except Exception as err:
    print(err)
# can book in another month
booking6 = booking_system.book_room(org2_default_user.id, org2.id, "Meet 6", room_1.id, datetime(2023, 8, 1, 12, 0), datetime(2023, 8, 1, 15, 0))
print("\norg2.booked_hours: ", org2.booked_hours)

# book again after cancelling another meet
booking_system.cancel_booking(org2_default_user.id, booking4.id)
booking5 = booking_system.book_room(org2_default_user.id, org2.id, "Meet 5", room_1.id, datetime(2023, 7, 6, 12, 0), datetime(2023, 7, 6, 22, 0))


rooms_found_1 = booking_system.find_rooms(org1_admin_user.id, building_1.id, floor_number=0, capacity=8, required_equipments=["monitor", "projector"])
print("\nrooms_found_1: ", rooms_found_1)
rooms_found_2 = booking_system.find_rooms(org1_admin_user.id, building_1.id, capacity=8, required_equipments=["monitor", "projector"])
print("\nrooms_found_2: ", rooms_found_2)

# any user can view organization bookings
org1_bookings = booking_system.get_organization_bookings(org1_admin_user.id, org1.id)
print("\norg1_bookings: ", org1_bookings)
org2_bookings = booking_system.get_organization_bookings(org2_default_user.id, org2.id)
print("\norg2_bookings: ", org2_bookings)
org1_default_user_bookings = booking_system.get_user_bookings(org1_default_user.id)
print("\norg1_default_user_bookings: ", org1_default_user_bookings)


