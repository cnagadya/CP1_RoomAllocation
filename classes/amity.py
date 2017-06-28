#! usr/bin/python3

import random
import os
import pickle
import term
from classes.person import Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import State, Base


class Amity( object ):
    def __init__(self):
        self.rooms = {"Offices": [], "Living Spaces": []}
        self.offices = {}
        self.living = {}
        self.people = []
        self.unallocated_office = []
        self.unaallocated_living = []

    def create_room(self, room_type, *room_names):
        """Method to create one or more rooms at the same time
           Required arguments: room_type and new_room_name:"""
        room_type = room_type.upper()
        for room_name in room_names:
            if room_name in self.rooms["Offices"] or room_name in self.rooms["Living Spaces"]:
                print( term.bold + "Room {} already exists".format( room_name ) + term.off )
            elif room_name.isalnum():
                if room_type == "OFFICE":
                    self.rooms["Offices"].append( room_name )
                    self.offices[room_name] = []
                    print( term.bggreen + "Office {} has been successfully created".format( room_name ) + term.off )
                elif room_type == "LIVING":
                    self.rooms["Living Spaces"].append( room_name )
                    self.living[room_name] = []
                    print(
                        term.bggreen + "Living space {} has been successfully created".format( room_name ) + term.off )
                else:
                    print( term.red + "WARNING!! Room Type can only be Office or Living" + term.off )
                    raise ValueError()

                    # print( ValueError )
            else:
                return term.red + "{} has not been added because it has special characters".format(
                    room_name ) + term.off

        return ""

    def add_person(self, first_name, last_name, person_type, wants_accommodation=None):
        """Method to add a person to the system and allocates the person to a random office (for both fellows &
           staff)  and living space if person is a fellow
           Required arguments:first_name, last_name &  person_type
           Optional arguments: wants_accommodation"""
        person_name = first_name + " " + last_name

        if len( self.rooms["Offices"] ) == 0 or len( self.rooms["Living Spaces"] ) == 0:
            return term.red + "You need to add at least one room and one office to add a person" + term.off

        elif person_type.upper() == "STAFF":
            print( "Adding {}...".format( person_name ) )
            if wants_accommodation is not None:
                return term.red + "For staff, you can only input 'First Name', 'Last Name' & 'Employment Type'" + term.off
            else:
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                # self.people[person_id] = person_name
                print( term.bggreen + "{} has successfully been added as a member of staff with id {}".format(
                    person_name, new_person.person_id ) + term.off )
                self.assign_office( new_person )

        elif person_type.upper() == "FELLOW":
            print( "Adding {}...".format( person_name ) )
            if wants_accommodation in ("n", "N") or wants_accommodation is None:
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                # self.people[person_id] = person_name
                print( term.bggreen + "{} has successfully been added as a fellow with id {}".format( person_name,
                                                                                                      new_person.person_id ) + term.off )
                self.assign_office( new_person )
                return "{} does not want accommodation".format( person_name )

            elif wants_accommodation.upper() == "Y":
                person_id = len( self.people ) + 1
                new_person = Person( person_name, person_type, person_id )
                self.people.append( new_person )
                print( term.bggreen + "{} has successfully been added as a fellow with id {}".format( person_name,
                                                                                                      new_person.person_id ) + term.off )
                self.assign_office( new_person )
                self.assign_living( new_person )

            else:
                return term.red + "Sorry, the value for 'wants_accommodation' can only be 'Y', 'N'or left blank" + term.off
        else:
            print( "{} not added because (s)he is neither a staff nor a fellow".format( person_name ) )
        return ("==============")

    def assign_office(self, new_person):
        """Helper method to assign fellows and staff office space. This method is called inside the add_person method"""

        choice_office = random.choice( list( self.offices.keys() ) )
        if len( self.offices[choice_office] ) < 6:
            self.offices[choice_office].append( new_person )
            print( "{} has been given an office {}".format(
                new_person.person_name, choice_office ) )
        else:
            self.unallocated_office.append( new_person )
            print( "{} has not been assigned an office because all are full.".format( new_person.person_name ) )

    def assign_living(self, new_fellow):
        """Helper method to assign fellows living spaces. This method is called inside the add_person method"""
        choice_living = random.choice( list( self.living.keys() ) )
        if len( self.living[choice_living] ) < 4:
            self.living[choice_living].append( new_fellow )
            print( "{} has been given accommodation in {}".format(
                new_fellow.person_name, choice_living ) )
        else:
            print( "{} has not been assigned a living space because all are full.".format( new_fellow.person_name ) )
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
                        return ("{} is already in {} and therefore cant be reallocated".format(
                            person.person_name, new_room_name ))
                    else:

                        if len( self.offices[new_room_name] ) < 6:
                            for room_name, occupants in self.offices.items():
                                if person in occupants:
                                    self.offices[room_name].remove( person )
                            self.offices[new_room_name].append( person )
                            print(
                                "{}'s office has been changed to '{}'".format( person.person_name, new_room_name ) )
                        else:
                            return "Sorry, office '{}' is already full".format( new_room_name )

                elif new_room_name in self.rooms["Living Spaces"]:
                    if person.person_type.upper() == "STAFF":
                        return ("A staff can not be allocated a living space")
                    else:
                        if person in self.living[new_room_name]:
                            print( "{} is already in {} and therefore cant be reallocated".format( person.person_name,
                                                                                                   new_room_name ) )
                        else:
                            if len( self.living[new_room_name] ) < 4:
                                for room_name, occupants in self.living.items():
                                    if person in occupants:
                                        self.living[room_name].remove( person )
                                self.living[new_room_name].append( person )
                                print( "{}'s living space has been changed to '{}'".format(
                                    person.person_name, new_room_name ) )
                            else:
                                return "Sorry, living space '{}' is already full".format( new_room_name )

                else:
                    return ("There is no room with name {} in the system".format(
                        new_room_name ))
        else:
            return ("No person with id {} exists in the system".format( person_id ))

            # return ("==============")

    def load_people(self, file_name):
        """Method takes a file as the input and adds the people  line by line into the system using the add_person
           method.
           Required arguments: file_name"""
        if len( self.rooms["Offices"] ) == 0 or len( self.rooms["Living Spaces"] ) == 0:
            return "You need to add atleast one room and one office to add a person"
        else:
            try:
                file = open( ('static/' + file_name), 'r' )
            except IOError:
                return "\n No file named {} exists".format( file_name )
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
        """Method prints out all rooms in the Dojo, (both the offices and living spaces) as well as the people in
           each room to the screen to the screen.
           Optional arguments: file_name. If specified, the unallocated people are saved to the file """

        if len( self.rooms["Offices"] ) == 0 and len( self.rooms["Living Spaces"] ) == 0:
            return "No offices or living spaces have been added to the system yet"
        else:
            if file_name is None:
                return self.allocations_view()
            else:
                with open( ('static/' + file_name), "w+" ) as file:
                    file.write( self.allocations_view() )
                return ("Allocations successfully saved to {}".format( file_name ))
        return ("==============")

    def allocations_view(self):
        """Helper method to filter out all people in the system that have been allocated to the different rooms"""
        allocations = ""
        for room_name in self.rooms["Offices"]:
            if self.offices[room_name]:
                allocations += "\nOffice Name: " + room_name + \
                               "\n-----------------------\nOccupants:\n"
                for person in (self.offices[room_name]):
                    allocations += str( person.person_id ) + \
                                   "." + person.person_name + "\n"
            else:
                allocations += "\n >> Office {} is empty!".format( room_name )
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
           Optional arguments: file_name. If specified, the unallocated people are saved to the file"""
        if self.unallocated_office == [] and self.unaallocated_living == []:
            return "There are no unallocated people in the system.\n =============="

        else:
            if not file_name:
                return (self.unallocated_view())
            elif file_name[-4:] not in [".doc", ".txt"]:
                return "Invalid file format! Data can only be saved to '.txt' or '.doc' files \n =============="
            else:
                with open( ('static/' + file_name), "w+" ) as file:
                    file.write( self.unallocated_view() )
                return "All unallocated people have been successfully saved to {} \n ==============".format( file_name )

    def unallocated_view(self):
        """Helper method to filter out all people in the system who havent been allocated living or office space """
        unallocated = ""
        if self.unallocated_office:
            unallocated += "\n People without offices\n---------------------\n"
            for person in self.unallocated_office:
                unallocated += str( person.person_id ) + "." + person.person_name + "\n"
        if self.unaallocated_living:
            unallocated += "\n People without Living Spaces\n---------------------\n"
            for person in self.unaallocated_living:
                unallocated += str( person.person_id ) + "." + person.person_name + "\n"
        return unallocated

    def print_room(self, room_name):
        """Method prints the names of all the people in  room_name  on the screen.
           Required arguments: room_name
        """
        if room_name in self.rooms["Offices"]:
            if self.offices[room_name]:
                print( "\n" + room_name + "\n-----------------------\n" )
                roomies = ""
                for person in self.offices[room_name]:
                    roomies += str( person.person_id ) + "." + person.person_name + "\n"
                return roomies
            else:
                return "Office {} is empty!".format( room_name )
        elif room_name in self.rooms["Living Spaces"]:
            if self.living[room_name]:
                print( "\n" + room_name + "\n---------------------\n" )
                roomies = ""
                for person in self.living[room_name]:
                    roomies += str( person.person_id ) + "." + person.person_name + "\n"
                return roomies
            else:
                return "Living Space {} is empty!".format( room_name )

        else:
            return "Room {} does not exist".format( room_name )

    def save_state(self, db_name):
        if self.rooms == {"Offices": [], "Living Spaces": []}:
            return "No data has been added to the app yet! \n =============="
        elif os.path.isfile( db_name ):
            return "Data not saved because a database with name {} already exists \n ==============".format( db_name )
        elif db_name[-3:] != ".db":
            return term.red + "\nInvalid format. File should have '.db' extension" + term.off
        else:
            engine = create_engine( 'sqlite:///{}'.format( db_name ) )
            Base.metadata.create_all( engine )
            Base.metadata.bind = engine
            DBSession = sessionmaker( bind=engine )
            session = DBSession()
            amity_data = (self.rooms, self.people, self.offices, self.living, self.unallocated_office,
                          self.unaallocated_living)
            app_state = pickle.dumps( amity_data )
            data_try = State( amity_state=app_state )
            session.add( data_try )
            session.commit()

            return term.bggreen + "Data has been saved to {}".format( db_name ) + term.off + "\n =============="

    def load_state(self, db_name):
        if os.path.isfile( db_name ):
            engine = create_engine( 'sqlite:///{}'.format( db_name ) )
            Base.metadata.bind = engine
            DBSession = sessionmaker()
            DBSession.bind = engine
            session = DBSession()
            query = session.query( State ).first()
            app_data = pickle.loads( query.amity_state )
            self.rooms, self.people, self.offices, self.living, self.unallocated_office, self.unaallocated_living = app_data
            return "Data in {} has been successfully loaded into the application \n==============".format( db_name )

        elif db_name[-3:] != ".db":
            return term.red + "\nInvalid format. File should have '.db' extension" + term.off

        else:
            return "Database {} does not exist".format( db_name ) + "\n =============="
