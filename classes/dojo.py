import term
import random


class Dojo( object ):
    """Dojo Superclass. All rooms are created within the dojo"""

    def __init__(self):
        Dojo.rooms = {}
        Dojo.offices = []
        Dojo.living = []

    def create_room(self, room_type, *room_names):
        """Method to create room in the dojo
        Takes arguments: room type (Office or Living) and atleast one room name
        """
        room_type = room_type.upper()
        if len( room_names ) < 1:
            return "create_room takes atleast two arguments, 'room_type' and 'room_name(s)'"
        else:
            if room_type == "OFFICE" or room_type == "LIVING":
                for room_name in room_names:
                    if room_name.isalpha():
                        if room_name not in Dojo.rooms:
                            Dojo.offices.append( room_name ) if room_type == "OFFICE" else Dojo.living.append(
                                room_name )
                            Dojo.rooms[room_name] = room_type

                            print( term.green + "{} called {} has been successfully created!"
                                                "".format( room_type, room_name ) + term.off )

                        else:
                            return "An office / living space with name {} already exists" \
                                   "".format( room_name )
                    else:
                        return term.red + "{} has not been added because it has special characters" \
                                          "".format( room_name ) + term.off

                        # return Dojo.rooms

            else:
                raise ValueError( "Room Type can only be Office or Living Space" )
                # print("invalid")


class Room( Dojo ):
    """subclass 'Room' that inherits from Dojo"""
    occupants = []
    # def __init__(self):super(Room, self).__init__()


class Office( Room ):
    """subclass office that inherits from room"""
    capacity = 6
    offices_dict = {}


    @classmethod
    def assign_office(cls, first_name):
        """Method to assign fellows and staff office space"""
        for office in Dojo.offices:
            cls.offices_dict[office] = []


        choice_office = random.choice( list( cls.offices_dict.values() ) )
        choice_office.append( first_name )
        print( '{} has been given an office'.format( first_name ) )
        return cls.offices_dict


dojo = Dojo()
dojo.create_room( "office", "Africa", "Australia", "Asia", "EWR^" )
dojo.create_room( "living", "Parrot", "Lion", "Impala", "Asia" )
