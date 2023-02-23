#!/usr/bin/env python3
import cmd
import sys
import hashlib
import json
from datetime import datetime
from blueprints.__init__ import storage
from blueprints.community import Community
from blueprints.issue import Issue
from blueprints.debate import Debate
from blueprints.user import User
from console_functions import create, update

class TheHorde(cmd.Cmd):
    """Contains the functionality for the HBNB console"""
    prompt = 'zombie:$ ' if sys.__stdin__.isatty() else ''
    classes = {'Community': Community, 'Issue': Issue,
               'Debate': Debate, 'User': User}
    
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    user = None
    
    def preloop(self) -> None:
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('zombie:$ Bye!')
        
    def precmd(self, line):
        """
        Usage: <class name>.<command>(<id>, {**kwargs})
        
        Note that you can either use <id> [<*args>] or
        <**kwargs> but never both and their presence being
        still dictated by the <dot_command>'s logic.
        Please note the syntax because the cmd is very strict
        and may not allow any deviation in terms of whitespace
        """
        try:
            if TheHorde.user is None:
                print("Please initialise user first using the `authorize` function. For help type `help authorize`")
                raise Exception
            else:
                pass
        except Exception as error:
            exit
            
    
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
            if command_ not in TheHorde.dot_cmds:
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
        """Method to exit the console"""
        exit()
    
    def help_quit():
        """Prints the help documentation for quit"""
        print("Exits the program without formatting. Usage: quit")
    
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

    def do_authorize(self, line):
        """
        Initialises a user session
        For logging in use:
        `authorize <id> <password>`
        if registering user:
        `authorize {
                    'id_number': <explanatory>,
                    'phone_number': <explanatory>,
                    'email': <ditto>,
                    'password': <ditto>
                    }
        `
        Note the last command has been indented and formatted for visual comprehension
        but it should all be in a single line
        """
        if line[0] == '{':
            try:
                new_user_params = json.loads(line)
            except json.JSONDecodeError:
                 print("Invalid dictionary. FAIL!")
                 return
            new_user = create.user(new_user_params)
            print(f"New user created of id: {new_user.id}")
            print("Please store this <id> in a safe place as it will be required every time you log in")
            TheHorde.user = new_user
            return
        processedLine = line.split(' ')
        id_ = processedLine[0]
        password = processedLine[0]
        try:
            user_instance = storage.all()[f'User.{id_}']
        except KeyError:
            "<id> does not exist. Try Again"
        
        password_hashed = hashlib.sha256(password.encode())
        hex_password = password_hashed.hexdigest()
        if hex_password == user_instance['password']:
            TheHorde.user = user_instance
        else:
            print("Wrong Password. Failed to initialise. Try Again")

    def do_create(self, line):
        """
        Create an object from any class
        Usage: 'create <class_name> {<**kwargs>}'
        **kwargs specification
        <Community>:
                    {'parent':<parent_name>, 'title':<community_title>}
        <Issue>:
                {'parent':<community_ancestral_name>, 'post': <post_string>}
        
        """
        if not line:
            print("<class_name> missing")
            return
        elements = line.partition(" ")
        class_ = elements[0]
        if class_ not in TheHorde.classes:
            print("<class_name> does not exist")
            return
        kwargs_ = " ".join(elements[1:])
        if len(kwargs_) < 2:
            print("Inadequate parameters. FAIL!")
            return
        try:
            kwargs_ = json.loads(kwargs_)
        except json.JSONDecodeError:
            print("Wrong input of parameters, please ensure that the parameters are enclosed in {} and is a legal dictionary.")
            return
        
        match class_:
            case "Community":
                newCommunity = create.community(kwargs_)
                storage.new(newCommunity)
                print(newCommunity.id)
            case "Issue":
                kwargs_['user_id'] = TheHorde.user.id
                newIssue = create.issue(kwargs_)
                storage.new(newIssue)
                print(newIssue.id)
            case _:
                print("Authorised. FAIL!")
                return

        
        storage.save()
    
    def do_show(self, line):
        """
        Method to show an individual object
        Usage: show <class_name> <object_id>
        """
        processedLine = line.split(" ")
        class_ = processedLine[0]
        id_ = processedLine[1]
        
        if not class_:
            print("Missing class name. FAIL!")
            return
        if class_ not in TheHorde.classes:
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
        This method destroys an object
        Usage: destroy <class_name> <id>
        """
        processedLine = line.split(" ")
        class_ = processedLine[0]
        id_ = processedLine[1]
        
        if not class_:
            print("Missing class name. FAIL!")
            return
        if class_ not in TheHorde.classes:
            print("Non-existent class. FAIL!")
            return
        if not id_:
            print("<id> missing. FAIL!")
            return
        object_name = class_ + '.' + id_
        try:
            del(storage.all()[object_name])
            storage.save()
        except KeyError:
            print("Instance does not exist. FAIL!")

    def do_all(self, line):
        """
        Shows all objects, or all objects of a class

        To show all objects:
        `all`
        To show all objects of specific class
        `all <ClassName>`
        """
        objects_list = []
        if line:
            class_ = line.split(" ")[0]
            if class_ not in TheHorde.classes:
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
        Counts the instances of a certain class
        
        Usage: count <class_name>
        """
        if not line or len(line) == 0:
            print("Missing class name. FAIL!")
        count = 0
        class_ = line.split(' ')[0]
        if class_ not in TheHorde.classes:
            print("Non-existent class. FAIL!")
        for key, value in storage.all().items():
            class_name = key.split('.')[0]
            if class_ == class_name:
                count += 1
        print(count)

    def do_update(self, line):
        """
        Updates a certain object with new data

        `Usage: update <class_name> <id> <**kwargs>`

        Please note that <kwargs> is a dictionary that is
        the dictionary that contains the keys and attributes of
        instance to update for acceptable parameters for different instances
        see below:
        <Community>:
                    {'parent':<parent_name>, 'title':<community_title>}
        <Issue>:
                {'parent':<community_ancestral_name>, 'post': <post_string>}
        <User>:
                {
                    'id_serial_number': <explanatory>,
                    'phone_number': <explanatory>,
                    'email': <ditto>,
                    'password': <ditto>
                }
        please note that the parameters are strict in that an unknown parameter cannot
        be updated to object
        Example:
        update Issue <someRandomId> {'parent': '<name_of_parent>'}
        This will update the parent attribute of Issue instance.
        """
        if line is None or len(line) < 1:
            print("Missing class name. Cannot update. FAIL")
            return
        preprocessed_line = line.split(' ')
        if len(preprocessed_line) < 2:
            print("Missing <id>. Cannot update. FAIL!")
            return
        class_ = preprocessed_line[0]
        if class_ not in TheHorde.classes:
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
        This command allows you to join a certain community
        Usage: `join <community_id>`
        """
        processed_line = line.split(' ')
        if line is None or len(processed_line) == 0:
            print("Please input <community_id>")
        community_id = processed_line[0]
        try:
            community_to_join = storage.all()[f'Community.{community_id}']
        except KeyError:
            print("Community does not exist. FAIL!")
            return
        if not community_to_join.addMember(TheHorde.user):
            print("FAILURE")
            return
        if not TheHorde.user.joinCommunity(community_id):
            print("Unrecognised error. Cancelling operation")
            community_to_join.removeMember(TheHorde.user)
        print("Communities you are part of:")
        User.communities_joined
        for community_ in TheHorde.user.communities_joined:
            print("\t+ {community_}")

if __name__ == "__main__":
    TheHorde().cmdloop()
