#! usr/bin/python3

import unittest
# import amity
from amity import Amity
from classes.person import Person, Staff, Fellow


class TestAmity( unittest.TestCase ):
    def setUp(self):
        self.amity = Amity()

    def test_create_single_office_successfully(self):
        self.amity.create_room( "Office", "Africa" )
        self.assertEqual( {"Offices": ["Africa"], "Living Spaces": []},
                          self.amity.rooms,
                          msg="Unable to create office!" )

    def test_create_single_living_successfully(self):
        self.amity.create_room( "Living", "Impala", "Eland" )
        self.assertEqual( {"Offices": [], "Living Spaces": ["Impala", "Eland"]},
                          self.amity.rooms,
                          msg="Unable to create living space!" )

    def test_create_two_living_successfully(self):
        self.amity.create_room( "Living", "Impala", "Eland" )
        self.assertEqual( {"Offices": [], "Living Spaces": ["Impala", "Eland"]},
                          self.amity.rooms,
                          msg="Unable to create multiple living spaces!" )

    def test_room_type_case_insensitive(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "office", "Asia" )
        self.amity.create_room( "OFFICE", "America" )
        self.amity.create_room( "OfFicE", "Europe" )
        self.assertEqual( {"Offices": ["Africa", "Asia", "America", "Europe"], "Living Spaces": []},
                          self.amity.rooms,
                          msg="Room Types are case sensitive!" )

    def test_office_name_has_special_characters(self):
        self.amity.create_room( "Office", "Afr!ca" )
        self.assertEqual( {"Offices": [], "Living Spaces": []},
                          self.amity.rooms,
                          msg="Offices with special character in name getting created!" )
        self.assertTrue( "Afr!ca has not been added because it has special characters",
                         self.amity.create_room( "Office", "Afr!ca" ) )

    def test_invalid_room_type(self):
        self.assertRaises( ValueError, self.amity.create_room,
                           "Off1ce", "Africa" )

    def test_repeated_office_name(self):
        repeated_name = self.amity.create_room( "Office", "Africa" )
        repeated_name
        self.assertEqual( {"Offices": ["Africa"], "Living Spaces": []},
                          self.amity.rooms )
        repeated_name
        self.assertNotEqual( {"Offices": ["Africa", "Africa"], "Living Spaces": []},
                             self.amity.rooms )

    def test_repeated_room_name_diff_type(self):
        self.amity.create_room( "Living", "Africa" )
        self.assertEqual( "An office / living space with name Africa already exists",
                          self.amity.create_room( "office", "Africa" ),
                          msg="Rooms with same names should not be created" )

    def test_staff_subclass(self):
        self.assertTrue( issubclass( Staff, Person ),
                         msg="Person has no subclass Staff!" )

    def test_add_person_no_rooms(self):
        self.assertEqual( "You need to add atleast one room and one office to add a person",
                          self.amity.add_person("Christine", "Nagadya", "STAFF" ),
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
        self.assertEqual( "Sorry, the value for 'wants_accommodation' can only be 'Y', 'N'or left blank",
                          self.amity.add_person( "Christine", "Nagadya", "Fellow", "Yes" ) )

    def test_add_staff_with_accommodation(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.assertEqual( "For staff, you can only input 'First Name', 'Last Name' & 'Employment Type'",
                          self.amity.add_person("Christine", "Nagadya", "STAFF", "Y" ),
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
        self.assertNotIn(self.amity.people[-1] , self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-2], self.amity.offices["Africa"] )
        self.assertIn(self.amity.people[-3],self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-4], self.amity.offices["Africa"] )
        self.assertIn(  self.amity.people[-5],self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-6], self.amity.offices["Africa"] )
        self.assertIn( self.amity.people[-7], self.amity.offices["Africa"] )

    def test_load_seven_people_in_file(self):
        initial_length = len(self.amity.people)
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.amity.load_people( 'names.txt' )
        final_length = len(self.amity.people)
        self.assertEqual(7, final_length -initial_length)

    def test_load_people_non_existent_file(self):
        self.amity.create_room( "Office", "Africa" )
        self.amity.create_room( "Living", "Brown" )
        self.assertEqual('Unable to locate file named namejs.txt',self.amity.load_people( 'namejs.txt' ),
                         msg = "Invalid file name")

    # def test_print_allocations_occupied_offices(self):
    #     pass
    #
    # def test_print_allocations_empty_offices(self):
    #     pass
    #
    # def test_print_allocations_to_file(self):
    #     pass
    #
    # def test_print_unallocated_no_file(self):
    #     pass
    #
    # def test_print_unallocated_all_allocated(self):
    #     pass
    #
    # def test_print_unallocated_to_file(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
