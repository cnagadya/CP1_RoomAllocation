class Person(object):
    def __init__(self, person_name, person_type, person_id):
        self.person_name = person_name
        self.person_type = person_type
        self.person_id = person_id

    def __repr__(self):
        return repr( self.person_name )


class Fellow( Person ):
    def __init__(self, person_name, person_type, person_id):
        super().__init__( person_name, person_type, person_id )
        self.person_type = "FELLOW"


class Staff( Person ):
    def __init__(self, person_name, person_type, person_id):
        super().__init__( person_name, person_type, person_id )
        self.person_type = "STAFF"
