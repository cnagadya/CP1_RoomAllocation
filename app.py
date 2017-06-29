"""Amity app: This is a command line app to digitize the allocation of offices and living spaces to staff and fellows
Usage:
amity create_room <room_type> <room_names>...
amity add_person <first_name> <last_name> <person_type> [<wants_accomodation>]
amity reallocate_person <person_id> <new_room_name>
amity load_people <file_name>
amity print_allocations [--file_name=None]
amity print_unallocated [--file_name=None]


amity (-h | --help)
amity --version
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
import cmd
import os
import term

from docopt import docopt, DocoptExit
from pyfiglet import Figlet

from classes.amity import Amity

amity = Amity()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            msg = "Invalid command! See help."
            print(msg)
            print(e)
            return

        except SystemExit:
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)

    return fn


def intro():
    print(__doc__)


class DojoRoomAllocation(cmd.Cmd):
    os.system("clear")

    f = Figlet(font='cosmic')
    print(term.white + f.renderText('A  M  I  T  Y') + term.off)
    print("=====================\n \n \n Type 'help' to view list of commands\n\n\n=====================\n")

    prompt = '\n ==== > Enter command: '
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_names>...
        """
        try:
            for room_name in arg['<room_names>']:
                print(amity.create_room(arg['<room_type>'], room_name))
                print("==============")
        except Exception:
            msg = term.red + 'An error when running create_room command' + term.off
            print(msg)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage:
        add_person <first_name> <last_name> <person_type> [<wants_accomodation>]
        """
        try:
            first_name = arg["<first_name>"]
            last_name = arg["<last_name>"]
            person_type = arg["<person_type>"]
            wants_accomodation = arg["<wants_accomodation>"]
            print(amity.add_person(first_name, last_name, person_type, wants_accomodation))

        except Exception:
            msg = term.red + 'An error when running add_person command' + term.off

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage:
                reallocate_person <person_id> <new_room_name>
                """
        try:
            person_id = arg["<person_id>"]
            new_room_name = arg["<new_room_name>"]
            print(amity.reallocate_person(int(person_id), new_room_name))
        except Exception:
            msg = term.red + 'An error when running reallocate_person command' + term.off

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage:
                load_people <file_name>
        """
        try:
            file_name = arg["<file_name>"]
            print(amity.load_people(file_name))
        except Exception:
            print(term.red + 'An error when running load_people command' + term.off)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage:
                print_allocations [--file_name=None]
        """
        try:
            file_name = arg["--file_name"]
            print(amity.print_allocations(file_name))
        except Exception:
            msg = term.red + 'An error when running print_allocations command' + term.off

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage:
                print_unallocated [--file_name=None]
        """
        try:
            file_name = arg["--file_name"]
            print(amity.print_unallocated(file_name))
        except Exception:
            msg = term.red + 'An error when running print_unallocated command' + term.off

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage:
                print_room <room_name>
        """
        try:
            room_name = arg["<room_name>"]
            print(amity.print_room(room_name))
            print("\n ==============")
        except Exception:
            print(term.red + 'An error when running print_room command' + term.off)

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage:
                save_state <db_name>
        """
        try:
            db_name = arg["<db_name>"]
            print(amity.save_state(db_name))
        except Exception:
            msg = term.red + 'An error when running save_state command' + term.off

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage:
                load_state <db_name>
        """
        try:
            db_name = arg["<db_name>"]
            print(amity.load_state(db_name))
        except Exception:
            msg = term.red + 'An error when running load_state command' + term.off

    def do_quit(self, arg):
        """Usage: quit

        """

        os.system('clear')
        print('\n=========================\n\nThank you for using the AMITY app. Hope to '
               'see you back soon\n\n=========================\n')
        exit()


DojoRoomAllocation().cmdloop()


# if __name__ == '__main__':
#     DojoRoomAllocation().cmdloop()
#
#  DojoRoomAllocation().cmdloop()
#  opt = docopt(__doc__,sys.argv[1:])
#  if opt["--interactive"]:
#      DojoRoomAllocation().cmdloop()
#      print(opt)
