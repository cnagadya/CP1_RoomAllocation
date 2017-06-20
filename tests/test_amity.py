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
                          self.amity.rooms)

    def test_repeated_room_name_diff_type(self):
        self.amity.create_room("Living", "Africa")
        self.assertEqual("An office / living space with name Africa already exists",
                         self.amity.create_room( "office", "Africa" ),
                         msg="Rooms with same names should not be created")

    def test_add_staff(self):
        self.amity.add_person("Christine", "Nagadya", "STAFF")
        self.amity.create_room("Office", "Africa")



if __name__ == '__main__':
    unittest.main()
