import random
from classes.dojo import Dojo, Office


class Person( object ):
    """Person superclass"""

    def __init__(self):
        self.people = []

    def add_person(self, first_name, last_name, person_type, wants_accomodation=None):
        """function to add a person. Requests for name & employment time"""
        person_type = person_type.upper()
        person_name = first_name + " " + last_name

        if person_type == "STAFF":
            if wants_accomodation is not None:
                return "For staff, you can only input 'First Name', 'Last Name' & 'Employment Type'"
            else:

                self.people.append( person_name )
                print( self.people )

                print( "{} has successfully been added as a {} ".format(
                    person_name, person_type ) )
                print( Office.assign_office(first_name ) )
        elif person_type == "FELLOW":
            if wants_accomodation == "N" or wants_accomodation is None:
                self.people.append( person_name )
                print( self.people )

                print( "{} has successfully been added as a {} ".format(
                    person_name, person_type ) + Office.assign_office( first_name ) )
                return ("{} does not want accomodation".format( person_name ))

            elif wants_accomodation == "Y":
                self.people.append( person_name )
                print( "{} has successfully been added as a {}".format(
                    person_name, person_type ) )
                print( "{} wants accomodation".format( person_name ) )
            else:
                return (
                    "Sorry, the value for 'wants_accomodation' can only be 'Y', 'N'or left blank")
            print( self.people )
        else:
            raise ValueError( "The person can only be a staff or fellow" )


class Staff( Person ):
    """Subclass of the Person Class.
       For People added as staff
    """
    pass


class Fellow( Person ):
    """Subclass of the Person Class.
       For People added as fellows
    """
    pass


person = Person()
person.add_person( "Joe", "Smith", "STAFF" )
person.add_person( "Nelson", "Mandela", "STAFF" )
person.add_person( "Christine", "Nagadya", "STAFF" )
person.add_person( "TI", "Andela", "STAFF" )
person.add_person( "Smith", "Smith", "STAFF" )
person.add_person( "Mandela", "Mandela", "STAFF" )
person.add_person( "Nagadya", "Nagadya", "STAFF" )
person.add_person( "Andela", "Andela", "STAFF" )

  