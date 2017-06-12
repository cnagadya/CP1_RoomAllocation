"""Dojo office and living space allocation app

Usage:
dojo create_room <room_type> <room_names>...
dojo add_person <first_name> <last_name> <person_type> [wants_accomodation]

dojo (-h | --help)
dojo --version
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
from docopt import docopt, DocoptExit
import cmd, os, sys, term
from dojo import Dojo, Room, Office
from person import Person
dojo = Dojo()
person = Person()

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action
    """

    def fn(self, arg):
        try:
            opt = docopt( fn.__doc__, arg )
        except DocoptExit as e:
            msg = "Invalid command! See help."
            print( msg )
            print( e )
            return

        except SystemExit:
            return

        return func( self, opt )

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update( func.__dict__ )

    return fn


def intro():
    print( __doc__ )


class DojoRoomAllocation( cmd.Cmd ):
    os.system( "clear" )

    prompt = '\n ==== > DojoRoomAllocation: '
    dojo = Dojo()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_names>...
        """
        try:
            for room_name in arg['<room_names>']:
                print( dojo.create_room( arg['<room_type>'], room_name ) )
        except Exception:
            msg = term.red + 'An error when running create_room command' + term.off

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage:
        add_person <first_name> <last_name> <person_type> [--wants_accomodation=None]
        """
        try:
            first_name = arg["<first_name>"]
            last_name = arg["<last_name>"]
            person_type = arg["<person_type>"]
            wants_accomodation = arg["--wants_accomodation"]
            print(person.add_person(first_name, last_name, person_type, wants_accomodation))

        except Exception:
            msg = term.red + 'An error when running add_person command' + term.off

    def do_quit(self, arg):
        """Usage: quit

        """

        os.system( 'clear' )
        print( 'Thank you for using our app. Hope to see you back soon' )
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
