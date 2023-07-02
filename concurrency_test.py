from threading import Thread
from datetime import datetime, timedelta
import time

from entities.booking_system import BookingSystem
from entities.role import Role
from entities.user import User

# add some delay before calling the passed function
def add_delay(func, *args, **kwargs):
    time.sleep(2)
    func(*args, **kwargs)

super_admin_role = Role("super_admin", [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
org_admin_role = Role("org_admin", [2,5,8,11,13,14,15,16,17,18])
org_default_role = Role("org_user", [2,5,8,11,14,16,17,18])

super_admin_user = User(0, "super_admin_user", "super_admin@booking.com", "11", [super_admin_role])

booking_system = BookingSystem(super_admin_user)

org1 = booking_system.add_organization(super_admin_user.id, "org1", "contact@org1.com", "org1phone")
org1_admin_user = booking_system.add_user(super_admin_user.id, org1.id, "org1_admin_user", "org1_admin_user@org1.com", "12", [org_admin_role])

building_1 = booking_system.add_building(super_admin_user.id, "Building 1")

floor_0 = booking_system.add_floor(super_admin_user.id, building_1.id, 0)

room_1 = booking_system.add_room(super_admin_user.id, building_1.id, floor_0.id, "Room 1", 1, 10, {"monitor", "projector", "ac"})
room_2 = booking_system.add_room(super_admin_user.id, building_1.id, floor_0.id, "Room 2", 2, 5, {"projector"})

org2 = booking_system.add_organization(super_admin_user.id, "org2", "contact@org2.com", "org2phone")
org2_admin_user = booking_system.add_user(super_admin_user.id, org2.id, "org2_admin_user", "org2_admin_user@org2.com", "12", [org_admin_role])

threads = [
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 1 Meet 1", room_1.id, datetime(2023, 7, 1, 5, 0), datetime(2023, 7, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 1 Meet 2", room_1.id, datetime(2023, 7, 1, 5, 0), datetime(2023, 7, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 1 Meet 3", room_1.id, datetime(2023, 7, 1, 5, 0), datetime(2023, 7, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 1 Meet 4", room_1.id, datetime(2023, 7, 1, 5, 0), datetime(2023, 7, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 1 Meet 5", room_1.id, datetime(2023, 7, 1, 5, 0), datetime(2023, 7, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 1 Meet 6", room_1.id, datetime(2023, 7, 1, 5, 0), datetime(2023, 7, 1, 7, 0))),
    
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 1 Meet 1", room_2.id, datetime(2023, 7, 2, 5, 0), datetime(2023, 7, 2, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 1 Meet 2", room_2.id, datetime(2023, 7, 2, 5, 0), datetime(2023, 7, 2, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 1 Meet 3", room_2.id, datetime(2023, 7, 2, 5, 0), datetime(2023, 7, 2, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 1 Meet 4", room_2.id, datetime(2023, 7, 2, 5, 0), datetime(2023, 7, 2, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 1 Meet 5", room_2.id, datetime(2023, 7, 2, 5, 0), datetime(2023, 7, 2, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 1 Meet 6", room_2.id, datetime(2023, 7, 2, 5, 0), datetime(2023, 7, 2, 7, 0))),
]

for thread in threads:
    try:
        thread.start()
    except Exception as err:
        print(err)
    

for thread in threads:
    thread.join()

# After running both orgs should have 1 booking each....

# both orgs should only get 1 booking each
org1_bookings = booking_system.get_organization_bookings(org1_admin_user.id, org1.id)
print("org1_bookings: ", org1_bookings)

org2_bookings = booking_system.get_organization_bookings(org2_admin_user.id, org2.id)
print("org2_bookings: ", org2_bookings)


threads = [
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 2 Meet 1", room_1.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 2 Meet 1", room_1.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 2 Meet 2", room_1.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 2 Meet 2", room_1.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 2 Meet 3", room_1.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 2 Meet 3", room_1.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 2 Meet 4", room_2.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 2 Meet 4", room_2.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 2 Meet 5", room_2.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 2 Meet 5", room_2.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org1_admin_user.id, org1.id, "Org 1 Attempt 2 Meet 6", room_2.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
    Thread(target=add_delay, args=(booking_system.book_room, org2_admin_user.id, org2.id, "Org 2 Attempt 2 Meet 6", room_2.id, datetime(2023, 8, 1, 5, 0), datetime(2023, 8, 1, 7, 0))),
]



for thread in threads:
    try:
        thread.start()
    except Exception as err:
        print(err)
    
for thread in threads:
    thread.join()
    

# total 2 bookings should happen in total, any orgs can have both, or both can share
org1_bookings = booking_system.get_organization_bookings(org1_admin_user.id, org1.id)
print("org1_bookings: ", org1_bookings)

org2_bookings = booking_system.get_organization_bookings(org2_admin_user.id, org2.id)
print("org2_bookings: ", org2_bookings)


