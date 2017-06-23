#! usr/bin/python3

import random
import os
import pickle
import term
from classes.person import Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import State, Base


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
                    print (term.bggreen + "Office {} has been successfully created".format( room_name ) + term.off)
                elif room_type == "LIVING":
                    self.rooms["Living Spaces"].append( room_name )
                    self.living[room_name] = []
                    print (term.bggreen + "Living space {} has been successfully created".format( room_name ) + term.off)
                else:
                    print (term.red + "WARNING!! Room Type can only be Office or Living" + term.off)
                    raise ValueError( )
                    # print( ValueError )
            else:
                return term.red + "{} has not been added because it has special characters".format( room_name ) + term.off
        return ("==============")

    def add_person(self, first_name, last_name, person_type, wants_accommodation=None):
        """Method to add a person to the system and allocates the person to a random office (for both fellows &
           staff)  and living space if person is a fellow
           Required arguments:first_name, last_name &  person_type
           Optional arguments: wants_accommodation"""
        person_name = first_name + " " + last_name

        if len( self.rooms["Offices"] ) == 0 or len( self.rooms["Living Spaces"] ) == 0:
            return term.red + "You need to add atleast one room and one office to add a person" + term.off

        elif person_type.upper() == "STAFF":
            print( "Adding {}...".format( person_name ) )
            if wants_accommodation is not None:
                return term.red + "For staff, you can only input 'First Name', 'Last Name' & 'Employment Type'"+ term.off
            else:
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                # self.people[person_id] = person_name
                print( "{} has successfully been added as a member of staff with id {}".format(
                    person_name, new_person.person_id ) )
                self.assign_office( new_person )

        elif person_type.upper() == "FELLOW":
            print( "Adding {}...".format( person_name ) )
            if wants_accommodation in ("n", "N") or wants_accommodation is None:
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                # self.people[person_id] = person_name
                print( "{} has successfully been added as a fellow with id {}".format(person_name, new_person.person_id ) )
                self.assign_office( new_person )
                return "{} does not want accommodation".format( person_name )

            elif wants_accommodation.upper() == "Y":
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                print( "{} has successfully been added as a fellow with id {}".format(person_name, new_person.person_id ))
                self.assign_office( new_person )
                self.assign_living( new_person )

            else:
                return (
                    "Sorry, the value for 'wants_accommodation' can only be 'Y', 'N'or left blank")
        else:
            print( "{} not added because (s)he is neither a staff nor a fellow".format(
                person_name ) )
        return( "==============" )


    def assign_office(self, new_person):
        """Helper method to assign fellows and staff office space. This method is called inside the add_person method"""

        choice_office = random.choice(list(self.offices.keys()))
        if len(self.offices[choice_office]) < 6:
            self.offices[choice_office].append(new_person)
            print("{} has been given an office {}".format(
                new_person.person_name, choice_office))
        else:
            self.unallocated_office.append(new_person)
            print("{} has not been assigned an office because all are full.".format(new_person.person_name))

    def assign_living(self, new_fellow):
        """Helper method to assign fellows living spaces. This method is called inside the add_person method"""
        choice_living = random.choice( list( self.living.keys() ) )
        if len( self.living[choice_living] ) < 4:
            self.living[choice_living].append( new_fellow )
            print( "{} has been given accommodation in {}".format(
                new_fellow.person_name, choice_living ) )
        else:
            print( "{} has not been assigned a living space because all are full.".format(new_fellow.person_name))
            self.unaallocated_living.append( new_fellow )

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
                        for room_name, occupants in self.offices.items():
                            if person in occupants:
                                self.offices[room_name].remove( person )
                        self.offices[new_room_name].append( person )
                        print(
                            "{}'s office has been changed to '{}'".format( person.person_name, new_room_name ) )
                        # break
                            # else:
                            #     print("{} did not have an office before and therefore cant be reallocated".format(person))
                            #     break


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
                            for room_name, occupants in self.living.items():
                                if person in occupants:
                                    self.living[room_name].remove( person )
                            self.living[new_room_name].append( person )
                            print( "{}'s living space has been changed to '{}'".format(
                                person.person_name, new_room_name ) )
                        else:
                            print( "Sorry, living space '{}' is already full".format(
                                new_room_name ) )

                else:
                    print( "There is no room with name {} in the system".format(
                        new_room_name ) )
        else:
            print( "No person with id {} exists in the system".format( person_id ) )

        return ("==============")

    def load_people(self, file_name):
        """Method takes a file as the input and adds the people  line by line into the system using the add_person
           method"""
        if len( self.rooms["Offices"] ) == 0 or len( self.rooms["Living Spaces"] ) == 0:
            return "You need to add atleast one room and one office to add a person"
        else:
            try:
                file = open( ('static/' + file_name), 'r' )
            except IOError:
                return "\nUnable to locate file named {}".format( file_name )
            else:

                line_no = 0
                for line in file:
                    line_no += 1
                    single_person = line.split()
                    if not single_person:
                        continue
                    elif len( single_person ) < 3 or len( single_person ) > 4:
                        print( "\nUnable to add person at line {}".format( line_no ) )
                    else:
                        first_name = single_person[0]
                        last_name = single_person[1]
                        person_type = single_person[2]
                        if len( single_person ) == 3:
                            wants_accommodation = None
                        else:
                            wants_accommodation = single_person[3]
                        print( "\n" )

                        self.add_person( first_name, last_name,
                                         person_type, wants_accommodation )


                print( "\nAll users in file {} added".format( file_name ) )
        return ("==============")

    def print_allocations(self, file_name=None):
        """Method prints out all rooms in the Dojo, (booth the offices and living spaces) as well as the people in
           each room to the screen to the screen.
           Optional arguments: file_name. Is specified, the unallocated people are saved to the file """

        if len( self.rooms["Offices"] ) == 0 or len( self.rooms["Living Spaces"] ) == 0:
            print( "No offices or living spaces have been added to the system yet" )
        else:
            if file_name is None:
                print( self.allocations_view() )
            else:
                with open( ('static/' + file_name), "w+" ) as file:
                    file.write( self.allocations_view() )
                print( "Allocations successfully saved to {}".format( file_name ) )
        return ("==============")

    def allocations_view(self):
        allocations = ""
        for room_name in self.rooms["Offices"]:
            if self.offices[room_name]:
                allocations += "\nOffice Name: " + room_name + \
                               "\n-----------------------\nOccupants:\n"
                for person in (self.offices[room_name]):
                    allocations += str( person.person_id ) + \
                                   "." + person.person_name + "\n"
            else:
                allocations += "\nOffice {} is empty!".format( room_name )
        for room_name in self.rooms["Living Spaces"]:

            if self.living[room_name]:
                allocations += "\nLiving Space name: " + room_name + \
                               "\n---------------------\nOccupants:\n"
                for person in self.living[room_name]:
                    allocations += str( person.person_id ) + \
                                   "." + person.person_name + "\n"
            else:
                allocations += "\n >> Living space {} is empty!\n".format( room_name )
        return allocations

    def print_unallocated(self, file_name=None):
        """Method prints a list of unallocated people to the screen.
           Optional arguments: file_name. Is specified, the unallocated people are saved to the file"""
        if self.unallocated_office == [] and self.unaallocated_living == []:
            print(
                "All people in the system have been allocated office and / or living space" )

        else:
            if not file_name:

                print( self.unallocated_view() )
            else:
                with open( ('static/' + file_name), "w+" ) as file:
                    file.write( self.unallocated_view() )
                print(
                    "All unallocated people have been successfully saved to {}".format( file_name ) )

    def unallocated_view(self):
        unallocated = ""
        unallocated += "\n People without offices\n---------------------"
        for person in self.unallocated_office:
            unallocated += "\n" + str( person )
        unallocated += "\n People without Living Spaces\n---------------------"
        for person in self.unaallocated_living:
            unallocated += "\n" + str( person )
        return unallocated

    def print_room(self, room_name):
        """Method prints the names of all the people in  room_name  on the screen.
           Required arguments: room_name
        """
        if room_name in self.rooms["Offices"]:
            if self.offices[room_name]:
                print( "\n" + room_name + "\n-----------------------\n" +
                       str( self.offices[room_name] ) )
            else:
                print( "{} is empty!".format( room_name ) )
        elif room_name in self.rooms["Living Spaces"]:
            if self.living[room_name]:
                print( "\n" + room_name + "\n---------------------\n" +
                       str( self.living[room_name] ) )
            else:
                print( "{} is empty!".format( room_name ) )

        else:
            print(
                "Sorry, no office or living space with name {} exists".format( room_name ) )
        return " =============="

    def save_state(self, db_name):
        if os.path.isfile( db_name ):
            return "Data not saved because a database with name {} already exists \n ==============".format( db_name )
        else:
            engine = create_engine( 'sqlite:///{}'.format( db_name ) )
            Base.metadata.create_all( engine )
            Base.metadata.bind = engine
            DBSession = sessionmaker( bind=engine )
            session = DBSession()
            amity_data = (self.rooms,self.people, self.offices, self.living, self.unallocated_office,
                          self.unaallocated_living)
            app_state = pickle.dumps( amity_data )
            data_try = State( amity_state=app_state )
            session.add( data_try )
            session.commit()

            return "Data has been saved to {} \n ==============".format( db_name )

    def load_state(self, db_name):
        if os.path.isfile( db_name ):
            engine = create_engine( 'sqlite:///{}'.format( db_name ) )
            Base.metadata.bind = engine
            DBSession = sessionmaker()
            DBSession.bind = engine
            session = DBSession()
            query = session.query( State ).first()
            app_data = pickle.loads( query.amity_state )
            self.rooms,  self.people, self.offices, self.living, self.unallocated_office, self.unaallocated_living = app_data
            return "Data in {} has been successfully loaded \n==============".format( db_name )
        else:
            return "File {} does not exist \n ==============".format( db_name )


