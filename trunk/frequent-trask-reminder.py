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
__date__ = "$Date$"
__version__ = "$Rev$"
__email__ = "gradha@users.sourceforge.net"
__credits__ = ""


# Modules to be imported.
from elementtree.ElementTree import Element
from elementtree.ElementTree import ElementTree
from elementtree.ElementTree import SubElement
import os
import sys
import time


# Some globals.
HUMAN_VERSION = "0.1.0"
DAY_IN_SECONDS = float(24 * 60 * 60)


# Exception hierarchy.
class Error(Exception): pass
class Lookup_error(Error): pass


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

 %s -lc
 %s -a "Water the binary trees."
 %s -k 3
 %s -wc "Check http://gradha.sdf-eu.org/ for updates."
""" % (HUMAN_VERSION, binary_name, binary_name, binary_name,
        binary_name, binary_name)
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
    string, the action parameter (could be None) and the parameter
    critical, which is a boolean telling if completed tasks should
    not be shown.
    """
    import getopt
    if not argv:
        argv = sys.argv
 
    short_list = "hvla:k:w:c"
    long_list = ["help", "version", "list", "add", "kill", "work", "critical"]

    try:
        opts, args = getopt.getopt(argv[1:], short_list, long_list)
    except getopt.error, msg:
        print "Error processing command line: %s\n" % msg
        usage_information(4)

    if len(args) > 0:
        print "Unknown arguments: %s" % args
        usage_information(3)

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
        elif option in ("-c", "--critical"):
            critical = 1
 
    if not action:
        print "You have to specify at least one action."
        usage_information(1)

    return (action, action_param, critical)


def get_today():
    """Returns the string year-mm-dd using today's date."""
    t = time.localtime()
    return "%04d-%02d-%02d" % (t[0], t[1], t[2])


def create_empty_configuration_file(file_name):
    """Creates the empty configuration file used to track tasks."""
    root = Element("frequent-task-reminder")
    
    # Create the configuration element.
    SubElement(root, "configuration-list")

    # Create the future container of tasks.
    SubElement(root, "task-list")

    # Create the future container of work units.
    SubElement(root, "work-unit-list")
    
    # Finally write the xml file.
    ElementTree(root).write(file_name, encoding="latin1")
    print "Created empty configuration file '%s'." % file_name


def string_to_seconds(text_string):
    """Returns a string in format YYYY-MM-DD into seconds since epoch."""
    return time.mktime(time.strptime(text_string, "%Y-%m-%d"))
    

def find_units_done(tree_root):
    """Returns a dictionary with the number of days spent on each
    task. The keys of the dictionary are the tasks' id values,
    which are stored as plain text."""
    dic = {}
    for node in tree_root.getiterator("work-unit"):
        key = node.get("id")
        days_so_far = dic.get(key, 0)
        dic[key] = days_so_far + 1
    return dic


def list_tasks(tree_root, critical):
    """Lists all the tasks from an xml tree.

    If critical is true, only tasks that have pending work units
    will be listed.
    """
    # Calculate the number of days used on each task.
    units_done = find_units_done(tree_root)

    current_time = time.time()
    
    for node in tree_root.getiterator("task"):
        # Don't print the task if it was killed.
        if node.get("killed"):
            continue
            
        # Find out the number of work units done for the task.
        task_id = node.find("id").text
        date_in_string = node.find("starting-day").text
        date_in_seconds = string_to_seconds(date_in_string)
        assert current_time > date_in_seconds
        days = int((current_time - date_in_seconds) / DAY_IN_SECONDS)
        done = units_done.get(task_id, 0)

        # Don't show if the user doesn't want the details.
        if critical and days + 1 - done < 1:
            continue
        
        print "---"
        print "Task %s" % task_id
        print "Name '%s'" % node.find("name").text
        
        print "Started on %s, %d days ago" % (date_in_string, days)
        print "Work units done %d, remaining to be done %d" % (done,
            days + 1 - done)


def add_task(tree_root, task_name):
    """Adds (stripped) task_name to the tree_root."""

    # Get a new task id, higher than all previous ones.
    id_num = highest_task_id(tree_root) + 1
    assert id_num >= 0

    # Todo: verify task name. Should be non empty and not numeric only."

    # Create the task.
    tasklist = tree_root.find("task-list")
    task = SubElement(tasklist, "task")
    SubElement(task, "id").text = "%d" % id_num
    SubElement(task, "name").text = task_name.strip()
    SubElement(task, "starting-day").text = get_today()


def highest_task_id(tree_root):
    """Returns a number with the highest task id or -1."""
    highest = -1
    # Find the highest task id we already have.
    for node in tree_root.getiterator("task"):
        highest = max(highest, int(node.find("id").text))

    return highest


def kill_task(tree_root, task_name_or_id):
    """Marks the specified task as killed."""

    node = find_task(tree_root, task_name_or_id)
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
    """Adds a work unit to the specified task."""

    # Obtain the task id.
    node = find_task(tree_root, task_name_or_id)
    task_id = node.find("id").text

    # Create a work-unit for the found task.
    work_units = tree_root.find("work-unit-list")
    work_unit = SubElement(work_units, "work-unit")
    work_unit.set("id", task_id)
    work_unit.text = get_today()


def main_process(action, action_param, critical):
    """Does the main task of running the program.

    Action is a string of: list, add, kill, work. action_param
    is the related parameter to the action. If critical is true,
    only actions that have pending work units will be displayed in
    the output.
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
        else:
            assert "Unknown action '%s', params '%s'" % (action, action_param)
            pass
    except Lookup_error, msg:
        print msg
        sys.exit(5)

    # Save the changes to the configuration file.
    data.write(file_name)

    # After an action always show the results.
    list_tasks(data, critical)
        

if __name__ == "__main__":
    action, action_param, critical = process_command_line()
    main_process(action, action_param, critical)
