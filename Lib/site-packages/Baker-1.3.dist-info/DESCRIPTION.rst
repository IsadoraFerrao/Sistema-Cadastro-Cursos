History
=======

Version 1.3
    * Better Python 3 support.
    * Improved test coverage.
    * Fixed #22: *varargs are now displayed in command help.
    * Fixed annoying beavhior of *varargs help when no keyword
        arguments are present.

Version 1.2
    * Python 3 support!
    * Runs from Python 2.6 up to 3.2.
    * More unit tests.
    * Code coverage to 89%.
    * Single-letter arguments are now automatically added to shortopts.
    * Fixed #14: Unable to mix varargs and kwargs.

Version 1.1
	* ``baker.run()`` now prints the return value of the command function.
	* Command usage help now shows help for optional arguments.
	* Added options to ``baker.run()``.
	* Added ``baker.usage([commandname])``.
	* Added unit tests.
	* Fixed bugs.


Overview
========

Baker lets you easily add a command line interface to your Python functions
using a simple decorator, to create scripts with "sub-commands", similar to
Django's ``manage.py``, ``svn``, ``hg``, etc.::

	#!python
	import baker

	# An imaginary script full of useful Python functions

	@baker.command
	def set(name, value=None, overwrite=False):
		"""Sets the value of a key in the database.

		If you don't specify a value, the named key is deleted. Overwriting
		a value may not be visible to all clients until the next full sync.
		"""

	    db = get_database()
	    if overwrite or name not in db:
	        if value is None:
	        	db.delete(name)
	        	print "Deleted %s" % name
	        else:
	        	db.set(name, value)
	    		print "Set %s to %s" % (name, value)
	    else:
	    	print "Key exists!"

	@baker.command
	def get(name):
		"Prints the value of a key in the database."

		db = get_database()
		print db.get(name)

	baker.run()

You can then run the script and use your function names and parameters as the
command line interface, using ``optparse``-style options::

	$ script.py set alfa bravo
	Set alfa to bravo

	$ script.py set --overwrite alfa charlie
	Set alfa to charlie

	$ script.py get alfa
	charlie

	$ script.py --help

	Available commands:

	 get  Prints the value of a key in the database.
	 set  Sets the value of a key in the database

	Use "script.py <command> --help" for individual command help.

	$ script.py set --help

	Usage: script.py set <name> [<value>]

	Sets the value of a key in the database.

	    If you don't specify a value, the named key is deleted. Overwriting
		a value may not be visible to all clients until the next full sync.

	Options:

        --overwrite


Arguments
=========

Baker maps command line options to function parameters in the most natural way
available.

Bare arguments are used to fill in required parameters::

	@baker.command
	def test(a, b, c):
	  print "a=", a, "b=", b, "c=", c

	$ script.py test 1 2 3
	a= 1 b= 2 c= 3

``--option`` arguments are used to fill in keyword parameters. You can use
``--option value`` or ``--option=value``, as in optparse::

	@baker.command
	def test(key="C"):
		print "In the key of:", key

	$ script.py test
	In the key of: C
	$ script.py test --key A
	In the key of: A
	$ script.py test --key=Gb
	In the key of: Gb

Function parameters where the default is ``None`` are considered optional
arguments and will be filled if extra arguments are available. Otherwise,
extra bare arguments never fill in keyword parameters::

  	@baker.command
  	def test(start, end=None, sortby="time"):
  	  print "start=", start, "end=", end, "sort=", sortby

  	$ script.py --sortby name 1
  	start= 1 end= sortby= name
  	$ script.py 1 2
  	start= 1 end= 2 sortby= time

If a keyword parameter's default is an int or float, Baker will try to
convert the option's string to the same type::

  	@baker.command
  	def test(limit=10):
  		print type(limit)

  	$ script.py test --limit 10
  	<type 'int'>

If the default of a parameter is a boolean, the corresponding command line
option is a flag that sets the opposite of the default::

  	@baker.command
  	def test(name, verbose=False):
  	  if verbose: print "Opening", name

  	$ script.py test --verbose alfa
  	Opening alfa

If the function takes ``*`` and/or ``**`` parameters, any leftover arguments
and options will fill them in.


Parameter help
==============

Baker lets you specify help for parameters in three ways.

In the decorator::

	@baker.command(params={"force": "Delete even if the file exists"})
	def delete(filename, force=False):
		"Deletes a file."
		if force or not os.path.exists(filename):
			os.remove(filename)

In Python 3.x, you can use parameter annotations to associate doc strings
with parameters::

    @baker.command
    def delete(filename, force:"Delete even if the file exists."=False):
    	"Deletes a file."
		if force or not os.path.exists(filename):
			os.remove(filename)

Baker can parse the function's docstring for Sphinx-style ``:param`` blocks::

	@baker.command
	def delete(filename, force=False):
		"""Deletes a file.

		:param force: Delete even if the file exists.
		"""
		if force or not os.path.exists(filename):
			os.remove(filename)


Short options
=============

To allow single-character short options (e.g. ``-v`` for ``--verbose``), use
the ``shortopts`` keyword on the decorator::

	@baker.command(shortopts={"verbose": "v"}, params={"verbose", "Spew lots"})
	def test(verbose=False):
		pass

	$ script.py test --help

	Usage: script.py test

	Options:

	 -v --verbose  Spew lots

You can group multiple short flag options together (``-xvc``). You can also
optionally not put a space between a short option and its argument, for
example ``-nCASE`` instead of ``-n CASE``.


``run()`` function
==================

The ``run()`` function has a few useful options.

* ``argv``: the list of options to parse. Default is ``sys.argv``.
* ``main``: if True (the default), this function acts like the main function
  of the module -- it prints errors instead of raising exceptions, prints
  the return value of the command function, and exits with an error code on
  errors.
* ``help_on_error``: if True, when an error occurs, automatically prints
  the usage help after the error message. Default is False.
* ``outfile``, ``errorfile``, ``helpfile``: the files to use for output,
  errors, and usage help. Defaults are stdout, stderr, and stdout.
* ``errorcode``: if main=True and this value is not 0, calls ``sys.exit()``
  with this code in the event of an error


``usage()`` function
====================

Use the ``usage()`` function if you need to print the usage help
programmatically::

	# Print overall help
	baker.usage()

	# Print help for a command
	baker.usage("commandname")

	# Print to a file
	baker.usage("commandname", file=sys.stdout)


Miscellaneous
=============

Instead of ``baker.run()``, you can use ``baker.test()`` to print out how
Baker will call your function based on the given command line.

As in many UNIX command line utilities, if you specify a single hyphen
(``-``) as a bare argument, any subsequent arguments will not parsed as
options, even if they start with ``--``.

Commands are automatically given the same name as the decorated function.
To give a command a different name, use the ``name`` keyword on the
decorator. This is especially useful when the command name you want
isn't a valid Python identifier::

  	@baker.command(name="track-all")
  	def trackall():
  		pass

You can specify a "default" command that is used when the first argument
to the script doesn't look like a command name::

  	@baker.command(default=True)
  	def here(back=False):
  	  print "here! back=", back

  	@baker.command
  	def there(back=False):
  	  print "there! back=", back

  	$ script.py --back
  	here! back= True

The ``baker`` module contains a ``Baker`` class you can instantiate if you
don't want to use the global functions::

	mybaker = baker.Baker()

	@mybaker.command
	def test():
		print "hello"

	mybaker.run()


About Baker
===========

Created by Matt Chaput.

Released under the
`Apache 2.0 license <http://www.apache.org/licenses/LICENSE-2.0>`_

Please file bugs in the BitBucket issue tracker.

http://bitbucket.org/mchaput/baker


