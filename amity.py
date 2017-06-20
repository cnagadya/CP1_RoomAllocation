#! usr/bin/python3

import random
# from person import *

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
                    print( ValueError )
            else:
                return "{} has not been added because it has special characters".format( room_name )

    def add_person(self, first_name, last_name, person_type, wants_accommodation=None):
        """Method to add a person to the system and allocates the person to a random office (for both fellows &
           staff)  and living space if person is a fellow
           Required arguments:first_name, last_name &  person_type
           Optional arguments: wants_accommodation"""
        person_name = first_name + " " + last_name
        print( "Adding {}...".format( person_name ) )
        if len( self.rooms["Offices"] ) == 0 or len( self.rooms["Living Spaces"] ) == 0:
            print( "You need to add atleast one room and one office to add a person" )

        elif person_type.upper() == "STAFF":
            if wants_accommodation is not None:
                return "For staff, you can only input 'First Name', 'Last Name' & 'Employment Type'"
            else:
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                # self.people[person_id] = person_name
                print( "{} has successfully been added as a member of staff".format(
                    person_name ) )
                Amity.assign_office( new_person )



        elif person_type.upper() == "FELLOW":
            if wants_accommodation == "N" or wants_accommodation is None:
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                # self.people[person_id] = person_name
                print( "{} has successfully been added as a fellow".format( person_name ) )
                Amity.assign_office( new_person )
                print( "{} does not want accommodation".format( person_name ) )

            elif wants_accommodation == "Y":
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                print( "{} has successfully been added as a fellow".format( person_name ) )
                Amity.assign_office( new_person )
                Amity.assign_living( new_person )

            else:
                print(
                    "Sorry, the value for 'wants_accommodation' can only be 'Y', 'N'or left blank" )
        else:
            print( "{} not added because (s)he is neither a staff nor a fellow".format( person_name ) )
        print( "==============" )

    @staticmethod
    def assign_office(new_person):
        """Helper method to assign fellows and staff office space. This method is called inside the add_person method"""
        # amity = Amity()
        choice_office = random.choice( list( amity.offices.keys() ) )
        if len( amity.offices[choice_office] ) < 6:
            amity.offices[choice_office].append( new_person )
            print( "{} has been given an office {}".format(
                new_person.person_name, choice_office ) )
        else:
            print( "Sorry there are no more available offices." )
            amity.unallocated_office.append( new_person )

    @staticmethod
    def assign_living(new_fellow):
        """Helper method to assign fellows living spaces. This method is called inside the add_person method"""
        choice_living = random.choice( list( amity.living.keys() ) )
        if len( amity.living[choice_living] ) < 4:
            amity.living[choice_living].append( new_fellow )
            print( "{} has been given accommodation in {}".format(
                new_fellow.person_name, choice_living ) )
        else:
            print( "Sorry there are no more available living spaces." )
            amity.unaallocated_living.append( new_fellow )

    def reallocate_person(self, person_id, new_room_name):
        """Method moves people from one room to another. It ensures that only fellows can be reallocated living
           spaces and that the capacity of the new room is not exceeded.
           Required arguments: person_id and new_room_name:"""

        if person_id in (person.person_id for person in self.people):
            for person in self.people:
                if person_id != person.person_id:
                    continue
                if new_room_name in self.rooms["Offices"]:
                    if person in self.offices[new_room_name]:
                        print( "{} is already in {} and therefore cant be reallocated".format(
                            person.person_name, new_room_name ) )
                    elif len( self.offices[new_room_name] ) < 6:
                        # implementation for removing from old rooom

                        print( "{}s office has been changed to '{}'".format(
                            person.person_name, new_room_name ) )
                    else:
                        print( "Sorry, office '{}' is already full".format(
                            new_room_name ) )

                elif new_room_name in self.rooms["Living Spaces"]:
                    if person.person_type.upper() == "STAFF":
                        print( "A staff can not be allocated a living space" )
                    else:
                        if person in self.living[new_room_name]:
                            print( "{} is already in {} and therefore cant be reallocated".format( person.person_name,
                                                                                                   new_room_name ) )
                        elif len( self.living[new_room_name] ) < 4:
                            for room_name, occupants in Amity.living.items():
                                if person in occupants:
                                    self.living[room_name].remove( person )
                            self.living[new_room_name].append( person )
                            print( "{}s living space has been changed to '{}'".format(
                                person.person_name, new_room_name ) )
                        else:
                            print( "Sorry, living space '{}' is already full".format(
                                new_room_name ) )

                else:
                    print( "There is no office with name {} in the system".format(
                        new_room_name ) )
        else:
            print( "No person with id {} exists in the system".format( person_id ) )

    def load_people(self, file_name):
        """Method takes a file as the input and adds the people  line by line into the system using the add_person
           method"""
        file = open(('../static/'+ file_name), 'r')
        for line in file:
            single_person = line.split()
            if not single_person:
                continue
            elif len( single_person ) < 3:
                print( "Unable to add user at line" )
            else:
                first_name = single_person[0]
                last_name = single_person[1]
                person_type = single_person[2]
                if len( single_person ) == 3:
                    wants_accommodation = None
                else:
                    wants_accommodation = single_person[3]

                amity.add_person( first_name, last_name, person_type, wants_accommodation )

    def print_allocations(self):
        """Method prints out all rooms in the Dojo, (booth the offices and living spaces) as well as the people in
           each room to the screen to the screen.
           Optional arguments: file_name. Is specified, the unallocated people are saved to the file """
        if len( self.rooms["Offices"] ) == 0 or len( self.rooms["Living Spaces"] ) == 0:
            print( "No offices or living spaces have been added to the system yet" )
        else:
            for room_name in self.rooms["Offices"]:
                if amity.offices[room_name]:
                    print( "\nOffice Name: " + room_name + "\n-----------------------\n" )
                    for name in (amity.offices[room_name]):
                        print( name )
                else:
                    print( "\nOffice {} is empty!".format( room_name ) )
            for room_name in self.rooms["Living Spaces"]:

                if amity.living[room_name]:
                    print( "\nLiving Space name: " + room_name + "\n---------------------\n" + "Occupants:" )
                    for name in amity.living[room_name]:
                        print( name )
                else:
                    print( "\nLiving space {} is empty!".format( room_name ) )

                    # f- open("allocations.txt", "w")

    def print_unallocated(self):
        """Method prints a list of unallocated people to the screen.
           Optional arguments: file_name. Is specified, the unallocated people are saved to the file"""

        if self.unallocated_office or self.unaallocated_living:
            print( "\n People without offices\n---------------------" )
            for person in self.unallocated_office:
                print( person )
            print( "\n People without Living Spaces\n---------------------" )
            for person in self.unaallocated_living:
                print( person )
        else:
            print( "All people in the system have been allocated office and / or living space" )

    def print_room(self, room_name):
        """Method prints the names of all the people in  room_name  on the screen.
           Required arguments: room_name
        """
        if room_name in self.rooms["Offices"]:
            if self.offices[room_name]:
                print( "\n" + room_name + "\n-----------------------\n" + str( amity.offices[room_name] ) )
            else:
                print( "{} is empty!".format( room_name ) )
        elif room_name in self.rooms["Living Spaces"]:
            if self.living[room_name]:
                print( "\n" + room_name + "\n---------------------\n" + str( amity.living[room_name] ) )
            else:
                print( "{} is empty!".format( room_name ) )

        else:
            print(
                "Sorry, no office or living space with name {} exists".format( room_name ) )

    def save_state(self, db_name):
        pass

    def load_state(self, db_name):
        pass


amity = Amity()
amity.create_room( "Office", "Blue", "Black", "Brown" )
amity.create_room( "Living", "Oranges", "Mangoes", "Apples" )
amity.load_people( 'names.txt')
amity.print_unallocated()
amity.print_allocations()
amity.print_room( "Mangoes" )
amity.reallocate_person( 4, "Brown" )
