# Author: Christine R N
import unittest
from classes.dojo import Dojo, Room
from classes.person import Person


class CreateRoomTestCase(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_room_subclass(self):
        self.assertTrue(issubclass(Room, Dojo),
                        msg="Dojo has no subclass Room!")

    def test_single_room_success(self):
        self.dojo.create_room("Living", "Africa")
        self.assertIn("Africa", self.dojo.rooms,
                      msg="Error in 'create_room' method when adding single room")

    def test_multiple_rooms_success(self):
        length1 = len(self.dojo.rooms)
        self.dojo.create_room("Office", "Africa", "Europe")
        length2 = len(self.dojo.rooms)
        self.assertEqual(length2 - length1, 2,
                         msg="Error in 'create_room' method when adding multiple rooms")

    def test_repeated_room(self):
        self.dojo.create_room("Living", "Africa")
        self.assertEqual(self.dojo.create_room("office", "Africa"),
                         "An office / living space with name Africa already exists",
                         msg="Rooms with same names should not be created")

    def test_invalid_room_type(self):
        self.assertRaises(ValueError, self.dojo.create_room,
                          "Living spae", "Australia")

    def test_room_name_isnt_alpha(self):
        invalid_roomname = self.dojo.create_room("Office", "Afr1ca")
        self.assertTrue(
            invalid_roomname, "Afr1ca has not been added because it has special characters")

    def test_less_than_3_args(self):
        self.assertEqual(self.dojo.create_room("office"),
                         "create_room takes atleast two arguments, 'room_type' and 'room_name(s)'"
                         )
        self.assertEqual(self.dojo.create_room("Africa"),
                         "create_room takes atleast two arguments, 'room_type' and 'room_name(s)'")


class CreatePersonTestCase(unittest.TestCase):
    def setUp(self):
        self.person = Person()
        self.dojo = Dojo()

    def test_add_staff_success(self):
        self.person.add_person("Joe", "Smith", "Staff")
        # self.dojo.create_room("Office", "Africa")
        # self.assertAlmostEqual(self.person.add_person("Joe", "Smith", "Staff"),
        #                  "Joe Smith has successfully been added as a STAFF Joe has been given an office",
        #                  msg="")
        self.assertIn("Joe Smith", self.person.people,
                      msg="Error in 'create_room' method when adding single room")

    def test_staff_want_accommodation(self):
        self.assertEqual(self.person.add_person("Joe", "Smith", "Staff", "YES"),
                         "For staff, you can only input 'First Name', 'Last Name' & 'Employment Type'",
                         msg="")

    def test_person_type_fail(self):
        self.assertRaises(ValueError, self.person.add_person,
                          "Joe", "Smith", "Saff")

    def test_fellow_accommodation_none(self):
        self.assertEqual(self.person.add_person("Joe", "Smith", "FEllow"),
                         "Joe Smith does not want accomodation",
                         msg="")

    def test_fellow_accommodation_invalid(self):
        self.assertEqual(self.person.add_person("Joe", "Smith", "FEllow", "P"),
                         "Sorry, the value for 'wants_accomodation' can only be 'Y', 'N'or left blank",
                         msg="")
