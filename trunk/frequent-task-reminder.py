#!/usr/bin/env python
# -*- mode:Python; tab-width: 4 -*-
"""Simple daily task reminder.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""

__author__ = "Grzegorz Adam Hankiewicz"
__date__ =  "$Date$"
__version__ = "$Rev$"
__email__ = "gradha@users.berlios.de"
__credits__ = ""


# Modules to be imported.
try:
    from elementtree.ElementTree import Element
    from elementtree.ElementTree import ElementTree
    from elementtree.ElementTree import SubElement
except ImportError:
    print "Oooops! Couldn't import the elementtree python package."
    print "You can download and install it from http://effbot.org/zone/element-index.htm"
    print
    raise
import os
import StringIO
import sys
import time


# Some globals.
HUMAN_VERSION = "0.1.1"
DAY_IN_SECONDS = float(24 * 60 * 60)


# Exception hierarchy.
class Error(Exception): pass
class Lookup_error(Error): pass
class Active_error(Error): pass


class Pretty_xml(StringIO.StringIO):
    """Wrapper to save XML files with human readable formatting.

    This little class wraps around a StringIO. ElementTree uses
    this class for saving, which will store the XML file as a string
    and then reformat it before storing it on disk.
    """
    def __init__(self, file_name):
        """Creates a memory StringIO for writting into filename."""
        self.file_name = file_name
        StringIO.StringIO.__init__(self)

    def close(self):
        """Saves the string to a file and releases the memory.

        TODO: Efficient regular expression substitution. This is ugly.
        """
        s = self.getvalue()
        StringIO.StringIO.close(self)
        s = s.replace("></frequent-task-reminder", ">\n</frequent-task-reminder")
        s = s.replace("><configuration-list", ">\n <configuration-list")
        s = s.replace("></configuration-list", ">\n </configuration-list")
        s = s.replace("><task-list", ">\n <task-list")
        s = s.replace("></task-list", ">\n </task-list")
        s = s.replace("><task", ">\n  <task")
        s = s.replace("></task", ">\n  </task")
        s = s.replace("><id", ">\n   <id")
        s = s.replace("><name", ">\n   <name")
        s = s.replace("><starting-day", ">\n   <starting-day")
        s = s.replace("><note", ">\n   <note")
        s = s.replace("><last-unit", ">\n   <last-unit")
        s = s.replace("", "")
        output_file = open(self.file_name, "wt")
        output_file.write(s)
        output_file.close()


def usage_information(exit_code = 0, binary_name = "frequent-task-reminder.py"):
    """Prints usage information and terminates execution."""
    print """Frequent task reminder %s.
Usage: %s command [options]

Commands:
    -l, --list
        List the tasks and their work units. Use this when you
        don't want to add, kill or modify existing tasks.
    -a x, --add x
        Adds a new task with name `x', starting today.
    -k x, --kill x
        Marks task `x' (id or name) as dead.
    -w x, --work x
        Adds one work unit to the task id/name `x'.
    -n x text, --note x text
        Modifies the task id/name `x' to have the note `text'. If
        there is no `text', the previous note will be erased.
Options:
    -h, --help
        Print this help screen.
    -v, --version
        Print only version number and exit.
    -c, --critical
        Ignore in output tasks which have 0 or less work units
        remaining. This can be used in all cases, since all commands
        output a list of tracked tasks.

You always have to provide an action to perform, but you can't
specify more than one action at the same time. Usage examples:

 %s --list -c
 %s -a "Water the binary trees."
 %s -kill 3
 %s -wc "Check http://gradha.sdf-eu.org/ for updates."
 %s -n "Water the binary trees." That was a joke
 %s --note 4
""" % (HUMAN_VERSION, binary_name, binary_name, binary_name,
        binary_name, binary_name, binary_name, binary_name)
    sys.exit(exit_code)


def process_command_line(argv = None):
    """Extracts from argv the options and returns them in a tuple.
 
    This function is a command line wrapper against main_process,
    it returns a tuple which you can `apply' calling main_process. If
    something in the command line is missing, the program will exit
    with a hopefully helpfull message.
 
    args should be a list with the full command line. If it is None
    or empty, the arguments will be extracted from sys.argv. The
    correct format of the accepted command line is documented by
    usage_information.

    The returned tuple will contain the action of the user as a
    string, the action parameter (could be None), the parameter
    critical, which is a boolean telling if completed tasks should
    not be shown, and the parameter text.
    """
    import getopt
    if not argv:
        argv = sys.argv
 
    short_list = "hvla:k:w:cn:"
    long_list = ["help", "version", "list", "add=", "kill=", "work=",
        "critical", "note="]

    try:
        opts, args = getopt.getopt(argv[1:], short_list, long_list)
    except getopt.error, msg:
        print "Error processing command line: %s\n" % msg
        usage_information(4)

    text = " ".join(args)

    def exit_if_action_is_defined(action):
        if action:
            print "You can't specify more than one action at a time."
            usage_information(2)
 
    # Default values
    action = None
    action_param = None
    critical = 0
    
    for option, value in opts:
        if option in ("-h", "--help"):
            usage_information()
        elif option in ("-v", "--version"):
            print HUMAN_VERSION
            sys.exit(0)
        elif option in ("-l", "--list"):
            exit_if_action_is_defined(action)
            action, action_param = "list", None
        elif option in ("-a", "--add"):
            exit_if_action_is_defined(action)
            action, action_param = "add", value
        elif option in ("-k", "--kill"):
            exit_if_action_is_defined(action)
            action, action_param = "kill", value
        elif option in ("-w", "--work"):
            exit_if_action_is_defined(action)
            action, action_param = "work", value
        elif option in ("-n", "--note"):
            exit_if_action_is_defined(action)
            action, action_param = "note", value
        elif option in ("-c", "--critical"):
            critical = 1
 
    if not action:
        print "You have to specify at least one action."
        usage_information(1)

    return (action, action_param, critical, text)


def get_today():
    """Returns the string year-mm-dd using today's UTC date."""
    t = time.gmtime(time.time())
    return "%04d-%02d-%02d" % (t[0], t[1], t[2])


def create_empty_configuration_file(file_name):
    """Creates the empty configuration file used to track tasks."""
    root = Element("frequent-task-reminder")
    
    # Create the configuration element.
    SubElement(root, "configuration-list")

    # Create the future container of tasks.
    SubElement(root, "task-list")

    # Finally write the xml file.
    ElementTree(root).write(file_name, encoding="latin1")
    print "Created empty configuration file '%s'." % file_name


def string_to_seconds(text_string):
    """Returns UTC string in format YYYY-MM-DD into seconds since epoch."""
    t = time.strptime(text_string, "%Y-%m-%d")
    # Set the daylight savings to zero. The default negative is evil.
    time_tuple = t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], 0
    return time.mktime(time_tuple) - time.timezone
    

def seconds_to_string(seconds):
    """Returns UTC YYYY-MM-DD string for the specified seconds since epoch."""
    return time.strftime("%Y-%m-%d", time.gmtime(seconds))
    
    
def list_tasks(tree_root, critical):
    """Lists all the tasks from an xml tree.

    If critical is true, only tasks that have pending work units
    will be listed.
    """
    current_time = time.time()
    
    for node in tree_root.getiterator("task"):
        # Don't print the task if it was killed.
        if node.get("killed"):
            continue
            
        # Find out the number of work units done for the task.
        task_id = node.find("id").text
        to_do = get_task_age(node, current_time)
        done = get_task_units_done(node)

        # Don't show if the user doesn't want the details.
        if critical and to_do - done < 1:
            continue

        print "---"
        line = "Task %s" % task_id
        line = line + " " * (15 - len(line))
        print line, node.find("name").text
        line = "Remaining %d" % (to_do - done)
        line = line + " " * (15 - len(line))
        print line,

        note_node = node.find("note")
        if note_node.text:
            print "Note: `%s'" % note_node.text
        else:
            print


def add_task(tree_root, task_name):
    """Adds (stripped) task_name to the tree_root."""
    assert task_name == task_name.strip()
    assert len(task_name) > 1

    # Get a new task id, higher than all previous ones.
    id_num = highest_task_id(tree_root) + 1
    assert id_num >= 0

    # Create the task.
    tasklist = tree_root.find("task-list")
    task = SubElement(tasklist, "task")
    SubElement(task, "id").text = "%d" % id_num
    SubElement(task, "name").text = task_name.strip()
    date_today = get_today()
    SubElement(task, "starting-day").text = date_today
    SubElement(task, "note").text = ""
    last_unit = SubElement(task, "last-unit", attrib = {"amount": "0"})
    last_unit.text = date_today


def highest_task_id(tree_root):
    """Returns a number with the highest task id or -1."""
    highest = -1
    # Find the highest task id we already have.
    for node in tree_root.getiterator("task"):
        highest = max(highest, int(node.find("id").text))

    return highest


def kill_task(tree_root, task_name_or_id):
    """Marks the specified task as killed. If the task was already
    killed, Active_error is thrown."""

    node = find_task(tree_root, task_name_or_id)
    if node.get("killed") == "yes":
        raise Active_error("Task %s is dead, aborting "
            "operation." % task_name_or_id)

    node.set("killed", "yes")


def find_task(tree_root, task_name_or_id):
    """Returns the node of the task, specified as name or id.

    If the task is not found, raises Lookup_error.
    """
    # Try to convert the given parameter to a number.
    text = task_name_or_id.strip()
    try:
        number = int(text)
        for node in tree_root.getiterator("task"):
            if int(node.find("id").text) == number:
                return node
    except ValueError:
        # Failed. In that case try with a name.
        for node in tree_root.getiterator("task"):
            if node.find("name").text == text:
                return node

    raise Lookup_error("Task with id/name '%s' not found." % text)

    
def add_work_unit_to_task(tree_root, task_name_or_id):
    """Adds a work unit to the specified task. If the task is not
    active, the operation throws Active_error."""

    node = find_task(tree_root, task_name_or_id)

    # If the task is killed, report it.
    if node.get("killed") == "yes":
        raise Active_error("Task %s is dead, aborting "
            "operation." % task_name_or_id)

    # Convert the last-unit date into UTC seconds.
    last_unit_node = node.find("last-unit")
    seconds = string_to_seconds(last_unit_node.text)
    # Don't forget about the amount value, which works like positive days.
    amount = int(last_unit_node.get("amount"))
    if amount > 0:
        seconds += (1 + amount) * DAY_IN_SECONDS
    else:
        seconds += DAY_IN_SECONDS
        
    # Now replace the current date and reset the amount attribute.
    new_text_date = seconds_to_string(seconds)
    assert last_unit_node.text != new_text_date
    last_unit_node.text = new_text_date
    last_unit_node.set("amount", "0")


def modify_task_note(tree_root, task_name_or_id, text):
    """Modifies the note field of a task."""

    node = find_task(tree_root, task_name_or_id)
    node.find("note").text = text
    

def advance_task_starting_date(task_node, days):
    """Moves the value of the starting date n days forward in time.

    The task's starting date will be increased in the specified
    number of days.
    """
    assert days > 0

    date = task_node.find("starting-day")
    date_in_string = date.text
    date_in_seconds = string_to_seconds(date_in_string)
    date_in_seconds += DAY_IN_SECONDS * days + 60 * 60 * 12 
    date.text = seconds_to_string(date_in_seconds)
    
        
def get_task_age(task_node, current_time):
    """f(task_node, current_time) -> work_units_to_do

    Returns the number of pending work units to be done for the
    specified tasks.  The number is calculated counting the number
    of days from starting-day to current_time.  When the starting-day
    task value and the current_time parameter are `in the same day',
    this function returns 1, assuming today's work unit has not
    been cleared yet.
    """
    date_in_string = task_node.find("starting-day").text
    date_in_seconds = string_to_seconds(date_in_string)
    # Now convert current_time to a YYYY-MM-DD.
    now = string_to_seconds(seconds_to_string(current_time))
    days = int((now - date_in_seconds) / DAY_IN_SECONDS)
    return 1 + days

    
def get_task_units_done(task_node):
    """f(task_node) -> work_units_done_so_far

    Returns the number of work units done since starting-day using
    the values of last-unit as reference.
    """
    # Get seconds of starting day.
    start = string_to_seconds(task_node.find("starting-day").text)
    
    # Convert the last-unit date into seconds.
    last_unit_node = task_node.find("last-unit")
    seconds = string_to_seconds(last_unit_node.text)
    # Don't forget about the amount value, which works like positive days.
    amount = int(last_unit_node.get("amount"))
    if amount > 0:
        seconds += amount * DAY_IN_SECONDS

    return int((seconds - start) / DAY_IN_SECONDS)
    

def main_process(action, action_param, critical, text):
    """Does the main task of running the program.

    Action is a string of: list, add, kill, work, note. action_param
    is the related parameter to the action. If critical is true,
    only actions that have pending work units will be displayed in
    the output. text is the optional text used in the note command.
    """
    file_name = os.path.expanduser("~/.frequent-task-reminderrc")
    if not os.path.isfile(file_name):
        create_empty_configuration_file(file_name)

    # Read the file.
    data = ElementTree(file = file_name)

    if "list" == action:
        list_tasks(data, critical)
        return

    try:
        if "add" == action:
            add_task(data, action_param)
        elif "kill" == action:
            kill_task(data, action_param)
        elif "work" == action:
            add_work_unit_to_task(data, action_param)
        elif "note" == action:
            modify_task_note(data, action_param, text)
        else:
            print "Unknown action '%s', params '%s'" % (action, action_param)
            sys.exit(4)
    except Lookup_error, msg:
        print msg
        sys.exit(5)
    except Active_error, msg:
        print msg
        sys.exit(6)

    # Save the changes to the configuration file.
    saver = Pretty_xml(file_name)
    data.write(saver)
    saver.close()

    # After an action always show the results.
    list_tasks(data, critical)
        

if __name__ == "__main__":
    action, action_param, critical, text = process_command_line()
    main_process(action, action_param, critical, text)
