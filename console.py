#!/usr/bin/env python3
import cmd
import sys
import hashlib
import json
from pprint import pprint
from datetime import datetime
from blueprints import storage
from blueprints.community import Community
from blueprints.issue import Issue
from blueprints.debate import Debate
from blueprints.user import User
from console_features import create, update, destroy
from blueprints.engine.ancestry import getIssuesOfCommunity
class TheHive(cmd.Cmd):
    """Contains the functionality for the HBNB console"""
    prompt = 'drone :$ ' if sys.__stdin__.isatty() else ''
    classes = {'Community': Community, 'Issue': Issue,
               'Debate': Debate, 'User': User}
    
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    user = None

    def checkIfUserIsInitialised(self):
         if TheHive.user is None:
                print("Please initialise user first using the `authorize` function. For help type `help authorize`")
                return False
         else:
             return True

    def preloop(self) -> None:
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('drone :$ Bye!')
        
    def precmd(self, line):
        """
        Usage: <class name>.<command>(<id>, {**kwargs})
        
        Note that you can either use <id> [<*args>] or
        <**kwargs> but never both and their presence being
        still dictated by the <dot_command>'s logic.
        Please note the syntax because the cmd is very strict
        and may not allow any deviation in terms of whitespace
        """
        command_ = class_ = id_ = args_ = '' # initialise line elements
        
        #scan for general reformatting - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line
        try: #parse line lefr to right
            pline = line[:]

            # isolate <class name>
            class_name_end = pline.find('.')
            class_ = pline[:class_name_end]

            # isolate and validate <command>
            command_end = pline.find('(')
            command_ = pline[class_name_end + 1: command_end]
            if command_ not in TheHive.dot_cmds:
                raise Exception
            
            # if paranthesis contain arguments, process them
            arguments_end = pline.find(')')
            arguments = pline[command_end + 1: arguments_end]
            if len(arguments) > 1:
                # isolate id
                if arguments.find(',') >= 0:
                    id_end = arguments.find(',')
                id_ = arguments[:id_end]

                # if arguments exist beyond _id
                if arguments.find('{'):
                    kwargs_start = arguments.find('{')
                    kwargs_ = arguments[kwargs_start:]
                    line = ' '.join([command_, class_, id_, kwargs_])
                
        except Exception as error:
            print("Failing: " + str(error))
        finally:
            return line
        
    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print("zombie:$ ")
        return stop
    def do_quit(self, command):
        """
        Exits the console
        -----------------
        """
        exit()
    
    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit()
    
    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program with formatting")
    
    def emptyline(self):
        """Overrides the emptyline method of Cmd"""
        pass

    def do_register(self, line):
        """
        Initialises a user session
        --------------------------

        + For logging in use:
            `authorize <id> <password>`

        + if registering user:
            `authorize 
                    {
                    "id_number": "12345678",
                    "phone_number": "+254#########",
                    "email": "the_horde@hotmail.com",
                    "password": "your_password_here"
                    }
        
        And for the love of the gods down below, don't put your password to be
        'your_password_here'


        - Note the command above has been indented and formatted for
          visual comprehension but it should all be in a single line
        
        - Also to ensure proper behaviour use double quotes for the
          strings
        """
        if line[0] == '{':
            try:
                new_user_params = json.loads(line)
            except json.JSONDecodeError as error:
                 print(f"{str(error)}\nFAIL!")
                 return
            new_user = create.user(new_user_params)
            print(f"New user created of id: {new_user.id}")
            print("Please store this <id> in a safe place as it will be required every time you log in")
            TheHive.user = new_user
            storage.new(new_user)
            storage.save()
            print("Thank you for joining us drone.")
            return
        else:
            print("Wrong json syntax.\n`help register` - for guidance")
            return

    def do_log_in(line):
        """
        Logs-in user
        ------------

        + For logging in use:
            `authorize <id_number> <password>`
        
        - Please note that we store both your id_number or your password as
          hashes

        - Don't enclose your args in quotes unless expressly stated in the
          help
        """
        processedLine = line.split(' ')
        id_number = processedLine[0]
        password = processedLine[1]
        
        id_number_hashed = hashlib.sha256(id_number_hashed.encode())
        id_number = id_number_hashed.hexdigest()
        
        try:
            user_instance = storage.all()[f'id_number']
        except KeyError:
            print("<id> does not exist. Try Again")
            return

        password_hashed = hashlib.sha256(password.encode())
        hex_password = password_hashed.hexdigest()
        if hex_password == user_instance.password:
            TheHive.user = user_instance
            print("Welcome back drone.")
        else:
            print("Wrong Password. Failed to initialise. Try Again")


    def do_create(self, line):
        """
        Create a Community or Issue object
        ----------------------------------

        + Usage:
            'create <class_name> {<**kwargs>}'
        
        
        <Community>:
                {"parent": "parent_name", "title": "community_title"}
        <Issue>:
                {"parent": "community_ancestral_name", "post": "post_string"}        
        """
        allowed_classes_for_create = {'Community': Community, 'Issue': Issue,
               'Debate': Debate}
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        if not line:
            print("<class_name> missing")
            return
        elements = line.partition(" ")
        class_ = elements[0]
        if class_ not in TheHive.classes:
            print("<class_name> does not exist")
            return
        kwargs_ = " ".join(elements[1:])
        if len(kwargs_) < 2:
            print("Inadequate parameters. FAIL!")
            return
        try:
            kwargs_ = json.loads(kwargs_)
        except json.JSONDecodeError as error:
            print(f"{str(error)}")
            return
        
        match class_:
            case "Community":
                newCommunity = create.community(kwargs_)
                if newCommunity is not None:
                    storage.new(newCommunity)
                    print(newCommunity.id)
            case "Issue":
                kwargs_['user_id'] = TheHive.user.id
                newIssue = create.issue(kwargs_)
                if newIssue is not None:
                    storage.new(newIssue)
                    print(newIssue.id)
            case _:
                print("Not Authorised. FAIL!")
                return

        
        storage.save()
    
    def do_show(self, line):
        """
        Displays an objects traits
        --------------------------

        + Usage:
            `show <class_name> <object_id>`
        """
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        processedLine = line.split(" ")
        class_ = processedLine[0]
        id_ = processedLine[1]
        
        if not class_:
            print("Missing class name. FAIL!")
            return
        if class_ not in TheHive.classes:
            print("Non-existent class. FAIL!")
            return
        if not id_:
            print("<id> missing. FAIL!")
            return
        object_name = class_ + '.' + id_
        try:
            print(storage.all()[object_name])
        except KeyError:
            print("Instance does not exist")
    

    def do_destroy(self, line):
        """
        Destroys an object
        ------------------

        + Usage:
            `destroy <class_name> <id>`
        """
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        processedLine = line.split(" ")
        class_ = processedLine[0]
        id_ = processedLine[1]
        
        if not class_:
            print("Missing class name. FAIL!")
            return
        if class_ not in TheHive.classes:
            print("Non-existent class. FAIL!")
            return
        if not id_:
            print("<id> missing. FAIL!")
            return
        match 'class_':
            case 'Community':
                destroy.communityBasedObject(class_, id_)
                return
            case 'Issue':
                destroy.communityBasedObject(class_, id_)
                return
            case _:
                destroy.communityBasedObject(class_, id_)

    def do_all(self, line):
        """
        Displays a collection of objects
        --------------------------------

        + To show all objects use:
            `all`
        
        + To show all objects of specific class

            `all <ClassName>`
        """
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        objects_list = []
        if line:
            class_ = line.split(" ")[0]
            if class_ not in TheHive.classes:
                print("Non-existent class. FAIL!")
                return
            for key, value in storage.all().items():
                class_name = key.split('.')[0]
                if class_name == class_:
                    objects_list.append(str(value))
        else:
            for key, value in storage.all().items():
                objects_list.append(str(value))
            
        print(objects_list)
    
    def do_count(self, line):
        """
        Counts number of objects of a class
        -----------------------------------
        
        + Usage:
            `count <class_name>`
        """
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        
        if not line or len(line) == 0:
            print("Missing class name. FAIL!")
        count = 0
        class_ = line.split(' ')[0]
        if class_ not in TheHive.classes:
            print("Non-existent class. FAIL!")
        for key, value in storage.all().items():
            class_name = key.split('.')[0]
            if class_ == class_name:
                count += 1
        print(count)

    def do_update(self, line):
        """
        Updates a specified object
        --------------------------

        + Usage: 
            `update <class_name> <id> <json>`

        json options
        ----------------
        - Do realize that these options are optional thus a dict can
          contain at a bare minimu only one key and value
        
        <Community>:
                {"parent": "parent_name", "title": "community_title"}
        <Issue>:
                {"parent": "community_ancestral_name", "post": "post_string"}
        <User>:
                {
                    "id_serial_number": "12345678",
                    "phone_number": "+254#########",
                    "email": "the_horde@hotmail.com",
                    "password": "your_password_here"
                }
        - please note that the parameters are strict in that an unknown parameter cannot
          be updated to object
        
        + Example:
            `update Issue <someRandomId> {"parent": "<name_of_parent>"}`
        This will update the parent attribute of Issue instance.
        """
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        if line is None or len(line) < 1:
            print("Missing class name. Cannot update. FAIL")
            return
        preprocessed_line = line.split(' ')
        if len(preprocessed_line) < 2:
            print("Missing <id>. Cannot update. FAIL!")
            return
        class_ = preprocessed_line[0]
        if class_ not in TheHive.classes:
            print("Non-existent class. FAIL!")
            return

        id_ = preprocessed_line[1]
        name_of_instance = class_ + '.' + id_
        if name_of_instance not in storage.all().keys():
            print("Instance not found. Cannot update. FAIL!")
            return
        parameters = preprocessed_line[2:]
        parameters = " ".join(parameters)
        parameters = json.loads(parameters)
        try:
            parameters = json.loads(parameters)
        except json.JSONDecodeError:
            print("Wrong input of parameters, please ensure that the parameters are enclosed in {} and is a legal dictionary.")
            return
        match class_:
            case "Community":
                updated_community = update.community(id_, parameters)
            case "Issue":
                updated_issue = update.issue(id_, parameters)
            case _:
                print("Object cannot be updated. UNAUTHORISED!")

    def do_join(self, line):
        """
        Joins the user to a community
        -----------------------------

        + Usage:
            `join <community_id>`
        """
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        processed_line = line.split(' ')
        if line is None or len(processed_line) == 0 or len(processed_line) > 1:
            print("Wrong input syntax. help join for guide.")
        community_id = line
        try:
            community_to_join = storage.all()[f'Community.{community_id}']
        except KeyError:
            print("Community does not exist. FAIL!")
            return
        if not community_to_join.addMember(TheHive.user):
            print("Failure trying to join community. Terminating operation.")
            return
        if not TheHive.user.joinCommunity(community_id):
            print("Unrecognised error. Cancelling operation")
            community_to_join.removeMember(TheHive.user)
            return
        print("Communities you are part of:")
        for community_ in TheHive.user.communities_joined:
            print("\t+ {community_}")
        
    def do_leave(self, line):
        """
        Cancel membership to a community
        --------------------------------

        + Usage:
            `leave <community_id>`
        """
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        processed_line = line.split(' ')
        if line is None or len(processed_line) == 0:
            print("Please input <community_id>")
        community_id = processed_line[0]
        try:
            community_to_join = storage.all()[f'Community.{community_id}']
        except KeyError:
            print("Community does not exist. FAIL!")
            return
        if not community_to_join.removeMember(TheHive.user):
            print("FAILURE")
            return
        if not TheHive.user.leaveCommunity(community_id):
            print("Unrecognised error. Cancelling operation")
            community_to_join.removeMember(TheHive.user)
        print("Communities you are part of:")
        for community_ in TheHive.user.communities_joined:
            print("\t+ {community_}")
        
    
    def do_for_you(self, line):
        """
        This function displays the a curated list of issues
        based on community

        PLEASE NOTE THIS FUNCTION IS STILL IN PRODUCTION, SO IT ONLY
        DISPLAYS A JSON OF ALL THE ISSUES RANKED ON TIME CREATED,
        OF ALL COMMUNITIES USER IS A MEMBER.
        
        -----------------------------------------------------------------
        
        FUTURE UPDATE OF THIS FUNCTION WILL INSTEAD WEIGHT THE ISSUES BASED
        ON VOTES_TALLY, TIME_CREATED, VOTES_FOR AND VOTES_AGAINST. 
        """
        if not self.checkIfUserIsInitialised():
            print("Please initialise user first using the `authorize` function. For help type `help authorize`")
            return
        current_user = TheHive.user
        user_communities_ids = current_user.communities_joined
        issues_dict = {}
        for community_id in user_communities_ids:
            community_instance = storage.all()[f'Community.{community_id}']
            community_name = community_instance.name
            issues_dict[community_name] = getIssuesOfCommunity(community_name)
        
        pprint(issues_dict)

if __name__ == "__main__":
    TheHive().cmdloop()
