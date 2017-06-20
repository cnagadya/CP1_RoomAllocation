#! usr/bin/python3
class Room( object ):
    def __init__(self, room_name, room_type, capacity):
        self.room_name = room_name
        self.room_type = room_type
        self.capacity = capacity


class Office( Room ):
    def __init__(self, room_name, room_type, capacity):
        super().__init__( room_name, room_type, capacity )
        self.capacity = 6


class LivingSpace( Room ):
    def __init__(self, room_name, room_type, capacity):
        super().__init__( room_name, room_type, capacity )
        self.capacity = 4