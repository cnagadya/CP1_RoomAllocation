#! usr/bin/python3
class Room( object ):
    def __init__(self, room_name):
        self.room_name = room_name



class Office( Room ):
    def __init__(self, room_name, room_type, capacity):
        Room.__init__(self, room_name )
        self.room_type = "Office"
        self.capacity = 6


class LivingSpace( Room ):
    def __init__(self, room_name, room_type, capacity):
        Room.__init__( room_name )
        self.room_type = "Living Space"
        self.capacity = 4