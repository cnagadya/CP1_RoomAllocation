import random
from classes.person import *


class Amity( object ):
    def __init__(self):
        self.rooms = {"Offices": [], "Living Spaces": []}
        self.offices = {}
        self.living = {}
        self.people = []
        self.unallocated_office = []
        self.unaallocated_living = []

    def create_room(self, room_type, *room_names):
        """Method to create one or more rooms at the same time"""
        room_type = room_type.upper()
        for room_name in room_names:
            if room_name in self.rooms["Offices"] or room_name in self.rooms["Living Spaces"]:
                return "An office / living space with name {} already exists".format( room_name )
            elif room_name.isalnum():
                if room_type == "OFFICE":
                    self.rooms["Offices"].append( room_name )
                    self.offices[room_name] = []
                elif room_type == "LIVING":
                    self.rooms["Living Spaces"].append( room_name )
                    self.living[room_name] = []
                else:
                    raise ValueError( "Room Type can only be Office or Living" )
            else:
                return "{} has not been added because it has special characters".format( room_name )

    def add_person(self, first_name, last_name, person_type, wants_accommodation=None):
        """function to add a person. Requests for name & employment type"""
        person_name = first_name + " " + last_name
        if len(self.rooms["Offices"]) == 0 and len(self.rooms["Living Spaces"]) == 0:
            print("You need to add atleast one room and one office to add a person")

        elif person_type.upper() == "STAFF":
            if wants_accommodation is not None:
                return "For staff, you can only input 'First Name', 'Last Name' & 'Employment Type'"
            else:
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                # self.people[person_id] = person_name
                print( "{} has successfully been added as a member of staff".format( person_name ) )
                Amity.assign_office( new_person )

                print( "==============" )

        elif person_type.upper() == "FELLOW":
            if wants_accommodation == "N" or wants_accommodation is None:
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                # self.people[person_id] = person_name
                print( "{} has successfully been added as a fellow".format( person_name ) )
                Amity.assign_office( new_person)
                print( "{} does not want accommodation".format( person_name ) )
                print( "==============" )
            elif wants_accommodation == "Y":
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                print( "{} has successfully been added as a fellow".format( person_name ) )
                Amity.assign_office( new_person )
                Amity.assign_living( new_person )
                print( "==============" )
            else:
                print( "Sorry, the value for 'wants_accommodation' can only be 'Y', 'N'or left blank" )
        else:
            print( "The person can only be a staff or fellow" )


    @staticmethod
    def assign_office(new_person):
        choice_office = random.choice( list( Amity.offices.keys() ) )
        if len( Amity.offices[choice_office] ) < 6:
            Amity.offices[choice_office].append( new_person )
            print( "{} has been given an office {}".format( new_person.person_name, choice_office ) )
        else:
            print( "Sorry there are no more available offices." )
            Amity.unallocated_office.append( new_person.person_name )

    @staticmethod
    def assign_living(new_fellow):
        choice_living = random.choice( list( Amity.living.keys() ) )
        if len( Amity.living[choice_living] ) < 4:
            Amity.living[choice_living].append( new_fellow )
            print( "{} has been given accommodation in {}".format( new_fellow.person_name, choice_living ) )
        else:
            print( "Sorry there are no more available living spaces." )

    def reallocate_person(self, person_id, new_room_name):
        if person_id in (person.person_id for person in self.people):
            for person in self.people:
                if person_id != person.person_id:
                    continue
                if new_room_name in self.rooms["Offices"]:
                    if person in Amity.offices[new_room_name]:
                        print( "{} is already in {} and therefore cant be reallocated".format( person, new_room_name ) )
                    elif len( Amity.offices[new_room_name] ) < 26:
                        # implementation for removing from old rooom
                        c
                        print( "{}s office has been changed to '{}'".format( person, new_room_name ) )
                    else:
                        print( "Sorry, office '{}' is already full".format( new_room_name ) )

                elif new_room_name in self.rooms["Living Spaces"]:
                    if person.person_type.upper() == "STAFF":
                        print( "A staff can not be allocated a living space" )
                    else:
                        if person in Amity.living[new_room_name]:
                            print( "{} is already in {} and therefore cant be reallocated".format( person,
                                                                                                   new_room_name ) )
                        elif len( Amity.living[new_room_name] ) < 4:
                            for room_name, occupants in Amity.living.items():
                                if person in occupants:
                                    Amity.living[room_name].remove( person )
                            Amity.living[new_room_name].append( person )
                            print( "{}s living space has been changed to '{}'".format( person, new_room_name ) )
                        else:
                            print( "Sorry, living space '{}' is already full".format( new_room_name ) )

                else:
                    print( "There is no office with name {} in the system".format( new_room_name ) )
        else:
            print( "No person with id {} exists in the system".format( person_id ) )

    def load_people(self, file_name):
        pass

    def print_allocations(self):
        pass

    def print_unallocated(self):
        pass

    def print_room(self, room_name):
        if room_name in self.rooms["Offices"]:
            print( room_name + "\n-----------------------\n" + str( Amity.offices[room_name] ) )
        elif room_name in self.rooms["Living Spaces"]:
            print( room_name + "\n---------------------\n" + str( Amity.living[room_name] ) )
        else:
            print( "Sorry, no office or living space with name {} exists".format( room_name ) )

    def save_state(self, db_name):
        pass

    def load_state(self, db_name):
        pass


class Room( object ):
    def __init__(self, capacity):
        self.capacity = capacity


class Office( Room ):
    def __init__(self, capacity):
        super().__init__( capacity )
        self.capacity = 6


class LivingSpace( Room ):
    def __init__(self, capacity):
        super().__init__( capacity )
        self.capacity = 4


