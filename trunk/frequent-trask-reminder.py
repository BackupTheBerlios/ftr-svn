#!/usr/bin/env python
# -*- mode:Python; tab-width: 4 -*-

# Modules to be imported.
from elementtree.ElementTree import Element
from elementtree.ElementTree import ElementTree
from elementtree.ElementTree import SubElement
import os
import time


# Some globals.
HUMAN_VERSION = "0.1.0"


def get_today():
    """Returns the string year-mm-dd using today's date."""
    t = time.localtime()
    return "%04d-%02d-%02d" % (t[0], t[1], t[2])


def create_empty_configuration_file(file_name):
    """Creates a default empty file with today's date as starting day."""
    root = Element("frequent-task-reminder")
    
    # Create the configuration element.
    config = SubElement(root, "configuration")
    
    # Create a default empty task.
    tasklist = SubElement(root, "tasklist")
    task = SubElement(tasklist, "task")
    SubElement(task, "id").text = 0
    SubElement(task, "name").text = "Default name"
    SubElement(task, "notes").text = "Some random notes you can modify."
    SubElement(task, "starting-day").text = get_today()
    
    # Finally write the xml file.
    ElementTree(root).write(file_name, encoding="latin1")
    print "Created empty configuration file '%s'." % file_name

    
def main():
    """Entry point of the binary."""
    file_name = os.path.expanduser("~/.frequent-task-reminderrc")
    if not os.path.isfile(file_name):
        create_empty_configuration_file(file_name)
        

if __name__ == "__main__":
    main()
