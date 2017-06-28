#! usr/bin/python3

import unittest
import term
import os
from classes.amity import Amity
from classes.person import Person, Staff, Fellow


class TestAmity( unittest.TestCase ):
    def setUp(self):
        self.amity = Amity()

    def test_create_room_single_office(self):
        self.amity.create_room( "Office", "Africa" )
        self.assertEqual( {"Offices": ["Africa"], "Living Spaces": []},
                          self.amity.rooms,
                          msg="Unable to create office!" )

    def test_create_room_single_living(self):
        self.amity.create_room( "Living", "Impala" )
        self.assertEqual( {"Offices": [], "Living Spaces": ["Impala"]},
                          self.amity.rooms,
                          msg="Unable to create living space!" )

    def test_create_room_multiple_living(self):
        self.amity.create_room( "Living", "Impala", "Eland" )
        self.assertEqual( {"Offices": [], "Living Spaces": ["Impala", "Eland"]},
                          self.amity.rooms,
                          msg="Unable to create multiple living spaces!" )

    def test_create_room_different_case(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "office", "Asia" )
        self.amity.create_room( "OFFICE", "America" )
        self.amity.create_room( "OfFicE", "Europe" )
        self.assertEqual( {"Offices": ["Africa", "Asia", "America", "Europe"], "Living Spaces": []},
                          self.amity.rooms,
                          msg="Room Types are case sensitive!" )

    def test_create_room_name_has_special_characters(self):
        self.amity.create_room( "Office", "Afr!ca" )
        self.assertEqual( {"Offices": [], "Living Spaces": []},
                          self.amity.rooms,
                          msg="Offices with special character in name getting created!" )
        self.assertTrue( "Afr!ca has not been added because it has special characters",
                         self.amity.create_room( "Office", "Afr!ca" ) )

    def test_create_room_invalid_room_type(self):
        self.assertRaises( ValueError, self.amity.create_room,
                           "Off1ce", "Africa" )

    def test_create_room_repeated_name_same_type(self):
        self.amity.create_room( "Office", "Africa" )
        self.assertEqual( {"Offices": ["Africa"], "Living Spaces": []}, self.amity.rooms )
        self.amity.create_room( "Office", "Africa" )
        self.assertNotEqual( {"Offices": ["Africa", "Africa"], "Living Spaces": []}, self.amity.rooms )

    def test_create_room_repeated_name_diff_type(self):
        self.amity.create_room( "Living", "Africa" )
        len1 = len( self.amity.rooms )
        self.amity.create_room( "Living", "Africa" )
        len2 = len( self.amity.rooms )
        self.assertEqual( len1,len2 ,
                          msg="Rooms with same names should not be created" )

    def test_staff_subclass(self):
        self.assertTrue( issubclass( Fellow, Person ),
                         msg="Person has no subclass Staff!" )
        self.assertIsInstance( Staff, type( Person ) )
    def test_fellow_subclass(self):
        self.assertTrue( issubclass( Fellow, Person ),
                         msg="Person has no subclass Fellow!" )
        self.assertIsInstance( Staff, type( Person ) )

    def test_add_person_no_rooms(self):
        self.assertEqual( term.red + "You need to add at least one room and one office to add a person" + term.off,
                          self.amity.add_person( "Christine", "Nagadya", "STAFF" ),
                          msg="Person can only be added if there is atleast one room and living space in the system" )

    def test_add_staff(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        christine = self.amity.people[-1]
        self.assertIn( christine, self.amity.offices["Africa"] )
        self.assertNotIn( christine, self.amity.living["Brown"] )

    def test_add_fellow_no_accommodation(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "Fellow" )
        christine = self.amity.people[-1]
        self.assertIn( christine, self.amity.offices["Africa"] )
        self.assertNotIn( christine, self.amity.living["Brown"] )
        self.assertEqual( "Christine Nagadya does not want accommodation",
                          self.amity.add_person( "Christine", "Nagadya", "Fellow" ),
                          msg="" )

    def test_add_fellow_with_accommodation(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "Fellow", 'Y' )
        christine = self.amity.people[-1]
        self.assertIn( christine, self.amity.offices["Africa"] )
        self.assertIn( christine, self.amity.living["Brown"] )

    def test_add_fellow_invalid_accommodation_option(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.assertIn( "Sorry, the value for 'wants_accommodation' can only be 'Y', 'N'or left blank",
                       self.amity.add_person( "Christine", "Nagadya", "Fellow", "Yes" ) )

    def test_add_staff_with_accommodation(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.assertEqual(
            term.red + "For staff, you can only input 'First Name', 'Last Name' & 'Employment Type'" + term.off,
            self.amity.add_person( "Christine", "Nagadya", "STAFF", "Y" ),
            msg="" )

    def test_add_more_staff_than_offices_can_accommodate(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.add_person( "SIMON", "PATTERSON", "STAFF" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "STAFF" )
        self.amity.add_person( "LEIGH ", "RILEY ", "STAFF" )
        self.amity.add_person( "ANA", "LOPEZ ", "STAFF" )
        self.amity.add_person( "KELLY", " McGUIRE ", "STAFF" )
        self.amity.add_person( "JOE", " SMITH ", "STAFF" )
        self.assertNotIn( self.amity.people[-1], self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-2], self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-3], self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-4], self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-5], self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-6], self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-7], self.amity.offices["Africa"] )

    def test_add_more_fellows_than_living_can_accommodate(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "FELLOW", "Y" )
        self.amity.add_person( "SIMON", "PATTERSON", "FELLOW", "Y" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "FELLOW", "Y" )
        self.amity.add_person( "LEIGH ", "RILEY ", "FELLOW", "Y" )
        self.amity.add_person( "ANA", "LOPEZ ", "FELLOW", "Y" )
        self.amity.add_person( "KELLY", " McGUIRE ", "FELLOW", "Y" )
        self.amity.add_person( "JOE", " SMITH ", "FELLOW", "Y" )
        self.assertNotIn( self.amity.people[-1], self.amity.living["Brown"] )

    def test_reallocate_person_to_new_office(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.create_room( "Office", "Asia" )
        self.amity.reallocate_person(1, "Asia" )
        self.assertIn( self.amity.people[-1],self.amity.offices["Asia"])
        self.assertNotIn( self.amity.people[-1],
                       self.amity.offices["Africa"] )

    def test_reallocate_fellow_to_new_living(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "Fellow" )
        self.amity.reallocate_person(1, "Brown" )
        self.assertIn( self.amity.people[-1],self.amity.living["Brown"])

    def test_reallocate_person_to_same_office(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.assertEqual("Christine Nagadya is already in Africa and therefore cant be reallocated",
                         self.amity.reallocate_person( 1, "Africa" ),
                         "Person should not be reallocated to a room he/she already occupies")

    def test_reallocate_person_staff_to_living(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.assertEqual("A staff can not be allocated a living space",
                         self.amity.reallocate_person( 1, "Brown" ),
                         "A staff cant have living space!")

    def test_reallocate_person_invalid_room(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.assertEqual("There is no room with name Asia in the system",
                         self.amity.reallocate_person( 1, "Asia" ),
                         "Cant reallocate to a non existent room")

    def test_reallocate_person_invalid_person_id(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.create_room("Office", "Asia")
        self.assertEqual("No person with id 2 exists in the system",
                         self.amity.reallocate_person( 2, "Asia" ),
                         "Cannot reallocate non existent person")

    def test_reallocate_person_office_full(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.create_room("Office", "Asia")
        self.amity.add_person( "SIMON", "PATTERSON", "STAFF" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "STAFF" )
        self.amity.add_person( "LEIGH ", "RILEY ", "STAFF" )
        self.amity.add_person( "ANA", "LOPEZ ", "STAFF" )
        self.amity.add_person( "SIMON", "PATTERSON", "STAFF" )
        self.amity.add_person( "SMITH  ", "JOE ", "STAFF" )
        self.amity.add_person( "LEIGH ", "RILEY ", "STAFF" )
        self.amity.add_person( "JOE", "LOPEZ ", "STAFF" )
        self.amity.add_person("PATTERSON", "SIMON",  "STAFF" )
        self.amity.add_person( "LAWRENCE ","MARI ",  "STAFF" )
        self.amity.add_person( "RILEY ","LEIGH ",  "STAFF" )
        self.amity.add_person("LOPEZ ",  "ANA", "STAFF" )
        self.assertIn("Sorry, office 'Asia' is already full",
                         self.amity.reallocate_person( 1, "Asia" ),
                         msg="Person cant be reallocated if destination office is full")

    def test_reallocate_person_living_full(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "FELLOW", "Y")
        self.amity.create_room( "Living", "Yellow" )
        self.amity.add_person( "Christine", "Nagadya", "FELLOW", "Y" )
        self.amity.add_person( "SIMON", "PATTERSON", "FELLOW", "Y" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "FELLOW", "Y" )
        self.amity.add_person( "LEIGH ", "RILEY ", "FELLOW", "Y" )
        self.amity.add_person( "ANA", "LOPEZ ", "FELLOW", "Y" )
        self.amity.add_person( "KELLY", " McGUIRE ", "FELLOW", "Y" )
        self.amity.add_person( "JOE", " SMITH ", "FELLOW", "Y" )
        self.amity.add_person( "LEIGH ", "RILEY ", "FELLOW", "Y" )
        self.assertIn( "Sorry, living space 'Yellow' is already full",
                       self.amity.reallocate_person( 1, "Yellow" ),
                       msg="Person cant be reallocated if destination office is full" )


    def test_load_seven_people_in_file(self):
        initial_length = len( self.amity.people )
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.load_people( 'names.txt' )
        final_length = len( self.amity.people )
        self.assertEqual( 7, final_length - initial_length )

    def test_load_people_non_existent_file(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.assertIn( 'No file named namejs.txt exists', self.amity.load_people( 'namejs.txt' ),
                       msg="Invalid file name" )

    def test_print_allocations_occupied_offices(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.assertIn( '1.Christine Nagadya', self.amity.print_allocations(),
                          msg="Room Occupants not printed to screen" )

    def test_print_allocations_occupied_living_space(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "Fellow", 'Y' )
        self.assertIn( '1.Christine Nagadya', self.amity.print_allocations(),
                          msg="Room Occupants not printed to screen" )

    def test_print_allocations_empty_office(self):
        self.amity.create_room( "Office", "Africa" )
        self.assertEqual('\n >> Office Africa is empty!', self.amity.print_allocations(),
                       msg="Notification for empty room" )

    def test_print_allocations_to_file(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.add_person( "SIMON", "PATTERSON", "STAFF" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "STAFF" )
        self.amity.add_person( "LEIGH ", "RILEY ", "STAFF" )
        self.amity.add_person( "ANA", "LOPEZ ", "STAFF" )
        self.assertEqual( 'Allocations successfully saved to allocations.txt',
                          self.amity.print_allocations("allocations.txt"),
                          msg="Allocations not saved to file" )

    def test_print_allocations_no_rooms(self):
        self.assertEqual( 'No offices or living spaces have been added to the system yet',
                          self.amity.print_allocations(),
                          msg="No rooms added notification" )

    def test_print_unallocated_to_screen(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.add_person( "SIMON", "PATTERSON", "STAFF" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "STAFF" )
        self.amity.add_person( "LEIGH ", "RILEY ", "STAFF" )
        self.amity.add_person( "ANA", "LOPEZ ", "STAFF" )
        self.amity.add_person( "KELLY", " McGUIRE ", "STAFF" )
        self.amity.add_person( "JOE", " SMITH ", "STAFF" )
        self.assertIn( "JOE  SMITH",
                       self.amity.print_unallocated(),
                       msg="Unallocated people not displayed to screen" )

    def test_print_unallocated_to_file(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.add_person( "SIMON", "PATTERSON", "STAFF" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "STAFF" )
        self.amity.add_person( "LEIGH ", "RILEY ", "STAFF" )
        self.amity.add_person( "ANA", "LOPEZ ", "STAFF" )
        self.amity.add_person( "KELLY", " McGUIRE ", "STAFF" )
        self.amity.add_person( "JOE", " SMITH ", "STAFF" )
        self.assertIn( "All unallocated people have been successfully saved to unallocated.txt",
                       self.amity.print_unallocated( "unallocated.txt" ),
                       msg="File for unallocated not created" )
        # os.remove("unallocated.txt")

    def test_print_unallocated_to_invalid_file(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.add_person( "SIMON", "PATTERSON", "STAFF" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "STAFF" )
        self.amity.add_person( "LEIGH ", "RILEY ", "STAFF" )
        self.amity.add_person( "ANA", "LOPEZ ", "STAFF" )
        self.amity.add_person( "KELLY", " McGUIRE ", "STAFF" )
        self.amity.add_person( "JOE", " SMITH ", "STAFF" )
        self.assertIn( "Invalid file format! Data can only be saved to '.txt' or '.doc' files",
                       self.amity.print_unallocated( "unallocated.mp4" ),
                       msg="Invalid file formats accepted" )

    def test_print_unallocated_no_unallocated(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.assertIn( "There are no unallocated people in the system.",
                       self.amity.print_unallocated(),
                       msg="Notified when all are allocated" )

    def test_print_room_office(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.assertIn( "Christine Nagadya",
                       self.amity.print_room( "Africa" ),
                       msg="People in given office not displayed to screen" )

    def test_print_room_living(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "Fellow", 'Y')
        self.assertIn( "Christine Nagadya",
                       self.amity.print_room( "Brown" ),
                       msg="People in given living space not displayed to screen" )

    def test_print_room_empty(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.assertIn( "Living Space Brown is empty",
                       self.amity.print_room( "Brown" ),
                       msg="People in given living space not displayed to screen" )

    def test_print_room_non_existent_room(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "Fellow", 'Y' )
        self.assertIn( "Room Africas does not exist",
                       self.amity.print_room( "Africas" ),
                       msg="No notification for invalid room name" )

    def test_save_state_no_data_in_app(self):
        self.assertIn( 'No data has been added to the app yet!',
                       self.amity.save_state( 'database.db' ),
                       msg='Empty app data saved!' )

    def test_save_state_data_saved_to_db(self):
        self.amity.create_room( "Office", "Africa" )
        self.assertIn( "Data has been saved to test.db",
                       self.amity.save_state( 'test.db' ),
                       msg='Data not saved to database' )
        os.remove( 'test.db' )  # to remove the created file after test is run

    def test_save_state_invalid_file(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.add_person( "Christine", "Nagadya", "STAFF" )
        self.amity.add_person( "SIMON", "PATTERSON", "STAFF" )
        self.amity.add_person( "MARI ", "LAWRENCE ", "STAFF" )
        self.assertEqual( term.red + "\nInvalid format. File should have '.db' extension" + term.off,
                          self.amity.save_state( 'database' ),
                          msg='Database files must have a ".db" extension' )

    def test_load_state_none_existent_file(self):
        self.assertIn( "Database test.db does not exist",
                       self.amity.load_state( 'test.db' ),
                       msg='Loading from not existent file' )

    def test_load_state_invalid_file(self):
        self.assertEqual( term.red + "\nInvalid format. File should have '.db' extension" + term.off,
                          self.amity.load_state( 'database' ),
                          msg='Data can only be loaded from files with a ".db" extension' )

    def test_load_state_from_file(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.save_state( 'test.db' )
        self.assertIn( "Data in test.db has been successfully loaded into the application ",
                       self.amity.load_state( 'test.db' ),
                       msg='Loading from not existent file' )
        os.remove( 'test.db' )


if __name__ == '__main__':
    unittest.main()
