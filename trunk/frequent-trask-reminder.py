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
DAY_IN_SECONDS = float(24 * 60 * 60)


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


def main():
    """Entry point of the binary."""
    file_name = os.path.expanduser("~/.frequent-task-reminderrc")
    if not os.path.isfile(file_name):
        create_empty_configuration_file(file_name)

    # Read the file.
    data = ElementTree(file = file_name)

    # Calculate the number of days used on each task.
    units_done = find_units_done(data)

    # Print how many tasks there are.
    print "Tracking %d task(s)." % len(data.getiterator("task"))
    for node in data.getiterator("task"):
        print "---"
        id = node.find("id").text
        print "Task %s" % id
        print "Name '%s'" % node.find("name").text
        
        date_in_string = node.find("starting-day").text
        date_in_seconds = string_to_seconds(date_in_string)
        current = time.time()
        assert current > date_in_seconds
        days = int((current - date_in_seconds) / DAY_IN_SECONDS)
        done = units_done.get(id, 0)
        
        print "Started on %s, %d days ago" % (date_in_string, days)
        print "Work units done %d, remaining to be done %d" % (done,
            days + 1 - done)
        

if __name__ == "__main__":
    main()
