#!/usr/bin/env python
# -*- mode:Python; tab-width: 4 -*-

# Modules to be imported.
import os
import time
from elementtree.ElementTree import Element, ElementTree, SubElement


# Some globals.
HUMAN_VERSION = "0.1.0"


def create_empty_configuration_file(file_name):
    """Creates a default empty file with today's date as starting day."""
    root = Element("frequent-task-reminder")
    
    # Create the configuration element.
    config = SubElement(root, "configuration")
    
    # Set the first day to track as today.
    start = SubElement(config, "starting-day")
    start.text = time.asctime()
    
    # Create a default empty task.
    tasklist = SubElement(root, "tasklist")
    task = SubElement(tasklist, "task")
    SubElement(task, "id").text = 0
    SubElement(task, "name").text = "Default name"
    SubElement(task, "notes").text = "Some random notes you can modify."
    
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
