# AMITY

> A simple command line  application to automate the allocation of offices and living spaces to people (either staff or fellows)

###### Application Functionalities
- [x] Create Room: A room can either be an **office or living space**. Depending on user preferences, one or more rooms of the same type can be created at a time
- [x] Add Person: A person, either **fellow or staff** can be added to the system and automatically allocated a room depending on his / her eligibility as well as room availabilty
- [x] Reallocate Person: A person can moved from one room to another
- [x] Load People: Multiple people can be loaded at once into the system from a test file
- [x] Print Allocations: The occupants of each room in the system can be displayed on the screen or saved to a text file
- [x] Print Unallocated: Fellows and Staff who have not yet been assigned office spaces and Fellows who requested for accommodation but are yet to be assigned can be displayed on the screen or saved to a test file
- [x] Print Room: Occupants of a given room of interest can be displayed to the screen
- [x] Save State: All application data can be saved to a database
- [x] Load State: Previously saved data can be loaded into the application


###### User Guide
1. Clone or download this repository to a computer that has python installed. Else download python [here](https://www.python.org/downloads/)
2. Install pip and virtual environment using the commands below, one after the other
```
easy_install pip
```
```
pip install virtualenv
```

3. Navigate to the application folder
4. Create a virtual environment for the project in the root folder using the command:
```
virtualenv venv
```
5. Activate the virtual environment using the command:
```
source venv/bin/activate
```
6. Install all the app dependencies listed in the requirements.txt file using the command:
```
pip install -r requirements.txt
```
7. And then executing the app.py file using:
```
python app.py
```
