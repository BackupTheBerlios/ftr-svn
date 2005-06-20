frequent-task-reminder
======================

Scenario description
--------------------

Every day you have to do repetitive tasks. Maybe you are keeping
an eye on some mirror. Maybe you check some web forum for specific
posts. Maybe you are working on a novel and try to make progress
on it every day.  Maybe you prefer the computer to remind you of
some task you otherwise manage to ignore. This program will remind
you of those boring tasks. Every day, in fact, every time you run it.

How does it work?
-----------------

frequent-task-reminder keeps a little "database" of pending tasks
in a file located at ~/.frequent-task-reminderrc. On the first run,
it will be created with pretty much a simple XML container. First you
have to add pending tasks you want this program to remind you. Then,
you call this script for example from your ~/.bash_profile, so it
is called every time you log into a console or open an xterm. Of
course, add the parameter --list to actually show the list of
tasks. And whenever you feel like, clear a pending work unit.

It's all very easy, and running the script without parameters
or with the --help parameter will show you the commandline usage
instructions.  Right now the program is limited to remind you of
tasks once per day. This is, every day the program adds a pending
work unit to all active tasks, which you have to clear. Since running
the script with the --critical option only shows the tasks without
cleared work units, this will show you what you still have to do
before the day is over.

Software requisites
-------------------

This software requires Python (http://www.python.org). It is
known to work with version 2.3.3. I haven't bothered too much
to make it work with previous versions, but if you need this,
I can make an efort and make it work with 1.5.2 or something
like that. You also need the ElementTree XML Python package from
http://effbot.org/zone/element-index.htm.

Usage
-----

frequent-task-reminder is for the time being a command line tool with a
few options. Run it with the ``-h`` or ``-help`` arguments and it will
tell you anything you need to know.

Usually you will end up putting this line somewhere in your
~/.bash_profile:

   path/to/where/you/untarred/this/frequent-task-reminder.py -lc

Contact information
-------------------

You should be able to get me through gradha@users.berlios.de. If
this fails, try going to my web page (currently at
http://gradha.sdf-eu.org/), my current email address is stamped at
the bottom of most pages. If that URL fails, you could try Googling
by "Grzegorz Adam Hankiewicz" (don't forget the quotes). Am I
narcissistic or what? As if you ever wanted to know that much...

License
-------

This software is covered under the GPL_. See the full license text
in the provided LICENSE file.

.. _GPL: http://www.gnu.org/licenses/licenses.html#GPL

