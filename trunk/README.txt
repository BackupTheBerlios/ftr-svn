frequent-task-reminder 0.2.0
============================

Scenario description
--------------------

Every day you have to do repetitive tasks. Maybe you are keeping
an eye on some mirror. Maybe you check some web forum for specific
posts. Maybe you are working on a book or essay and try to make
progress on it every day.  Maybe you prefer the computer to remind
you of some task you otherwise manage to ignore. This program will
remind you of those boring tasks. Every day. In fact, every time
you run it.

How does it work?
-----------------

frequent-task-reminder keeps a little *database* of pending tasks in
a file located at ``~/.frequent-task-reminderrc``. On the first run,
it will be created with pretty much a simple XML container. First you
have to add pending tasks you want this program to remind you. Then,
you call this script for example from your ``~/.bash_profile``, so
it is called every time you log into a console or open an xterm. Of
course, add the parameter ``--list`` to actually show the list of
tasks. And whenever you feel like, clear a pending work unit.

It's all very easy, and running the script without parameters or
with the ``--help`` parameter will show you the commandline usage
instructions.  Right now the program is limited to remind you of
tasks once per day. This is, every day the program adds a pending
work unit to all active tasks, which you have to clear. Since
running the script with the ``--critical`` option only shows the
tasks without cleared work units, this will show you what you still
have to do before the day is over.

Software requisites
-------------------

This software requires Python (http://www.python.org). It is
known to work with version 2.3.3. I haven't bothered too much
to make it work with previous versions, but if you need this,
I can make an efort and make it work with 1.5.2 or something
like that. You also need the ElementTree XML Python package from
http://effbot.org/zone/element-index.htm.

Usage examples
--------------

frequent-task-reminder is for the time being a command line tool
with a few options. Run it with the ``-h`` or ``-help`` arguments
and it will tell you anything you need to know.

Usually you will end up putting this line somewhere in your
~/.bash_profile::

   path/to/where/you/untarred/this/frequent-task-reminder.py -lc

The first thing you will want to do is create a new task::

   frequent-task-reminder.py -a "Visit http://photo.net/"

The task is created, and the program automatically lists all the
active tasks.  Your new task will have an numerid id, which can be
used later to handle work units.  Now, assuming you have done the
task for today, you want to clear the work unit with::

   frequent-task-reminder.py -w task_id/task_name

You can use the name of the task or the id, which is shorter and
quicker to type. Once the task is cleared to zero, just wait another
day and the counter will go up.

If you are wondering what kind of tasks this is good for, I do some
documentation cleanup tasks for a few free software projects. It is
as easy as taking the entry of a programming API and thinking how
would you improve the documentation. So each day I try to improve
the API and at the end of the week I see if I can send a patch to
the project with my changes.

Another one I do every day is documentation translation. The problem
with translations is that it's a very very very boring job. About
95% of people I've seen strarting a translation are gone after
a week. However, translating one or two paragraphs of text a day
takes less than five minutes. So that's all I do. At the end of the
month, I do more this way than saying "*Ah, I'll wait for a weekend
and work for an hour or two*", because I know (and you know) that
weekends are for other things and I'll want to rest.

Finally, another nice use I have for this program is reminding me
to read books. Depending on the book, my interest and free time, I
decide that one work unit is a few pages or a chapter.  This way I
have been reading up to five books simultaneously and none of them
really drag me down.  In fact, all the above takes about less than
half hour every day. I prefer to spend that time in various projects
than neglect something for a long time. If you think this way too,
you might find the program useful.

Downloads and contact information
---------------------------------

The web page for this script is at:

  http://ftr.berlios.de/

BerliOS also provides other services related to this project at:

  http://developer.berlios.de/projects/ftr/

You should be able to email me using gradha@users.berlios.de,
which is a forwarder to my real email address.

License
-------

This software is covered under the GPL_. See the full license text
in the provided LICENSE.txt file.

.. _GPL: http://www.gnu.org/licenses/licenses.html#GPL
