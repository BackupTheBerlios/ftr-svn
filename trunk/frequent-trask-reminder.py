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


def usage_information(exit_code = 0, binary_name = "frequent-task-reminder.py"):
    """Prints usage information and terminates execution."""
    print """Usage: %s [-hv -i xxx -o xxx]

-h, --help
   Print this help screen.
-v, --version
   Print version number and exit.


Usage examples:
 %s
""" % (binary_name, binary_name)
    sys.exit(exit_code)


def process_command_line(argv = None):
   """Extracts from argv the options and returns them in a tuple.

   Errrfff... update this to something usefull...

   This function is a command line wrapper against main_process,
   it returns a tuple which you can `apply' calling main_process. If
   something in the command line is missing, the program will exit
   with a hopefully helpfull message.

   args should be a list with the full command line. If it is None
   or empty, the arguments will be extracted from sys.argv. The
   correct format of the accepted command line is documented by
   usage_information.
   """
   import getopt
   if not argv:
      argv = sys.argv

   short_list = "hv"
   long_list = ["help", "version"]

   try:
      opts, args = getopt.getopt(argv[1:], short_list, long_list)
   except getopt.error, msg:
      print "Error processing command line: %s\n" % msg
      usage_information(2)

   for option, value in opts:
      if option in ("-h", "--help"):
         usage_information()
      elif option in ("-v", "--version"):
         print HUMAN_VERSION
         sys.exit(0)

   return None


def get_today():
    """Returns the string year-mm-dd using today's date."""
    t = time.localtime()
    return "%04d-%02d-%02d" % (t[0], t[1], t[2])


def create_empty_configuration_file(file_name):
    """Creates a default empty file with today's date as starting day."""
    root = Element("frequent-task-reminder")
    
    # Create the configuration element.
    SubElement(root, "configuration")
    
    # Create a default empty task.
    tasklist = SubElement(root, "tasklist")
    task = SubElement(tasklist, "task")
    SubElement(task, "id").text = "0"
    SubElement(task, "name").text = "Default name"
    SubElement(task, "starting-day").text = get_today()
    
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
        key = node.attrib["id"]
        days_so_far = dic.get(key, 0)
        dic[key] = days_so_far + 1
    return dic


def list_tasks(tree_root):
    """Lists all the tasks from an xml tree."""
    # Calculate the number of days used on each task.
    units_done = find_units_done(tree_root)

    current_time = time.time()
    
    # Print how many tasks there are.
    print "Tracking %d task(s)." % len(tree_root.getiterator("task"))
    for node in tree_root.getiterator("task"):
        print "---"
        task_id = node.find("id").text
        print "Task %s" % task_id
        print "Name '%s'" % node.find("name").text
        
        date_in_string = node.find("starting-day").text
        date_in_seconds = string_to_seconds(date_in_string)
        assert current_time > date_in_seconds
        days = int((current_time - date_in_seconds) / DAY_IN_SECONDS)
        done = units_done.get(task_id, 0)
        
        print "Started on %s, %d days ago" % (date_in_string, days)
        print "Work units done %d, remaining to be done %d" % (done,
            days + 1 - done)


def main_process():
    """Does the main task of running the program."""
    file_name = os.path.expanduser("~/.frequent-task-reminderrc")
    if not os.path.isfile(file_name):
        create_empty_configuration_file(file_name)

    # Read the file.
    data = ElementTree(file = file_name)

    list_tasks(data)
        

if __name__ == "__main__":
    process_command_line()
    main_process()
