.. highlight:: bash


User guide
==========

Installation
------------

::

    $ pip install mr.bobby


Usage
-----


Once you install mr.bobby, the ``mrbobby`` command is available::

    $ mrbobby --help
    usage: mrbobby [-h] [-O TARGET_DIRECTORY] [-v] [-c CONFIG] [-V] [-l] [-w] [-n]
                 [-q]
                 [template]

    Filesystem template renderer

    positional arguments:
      template              Template name to use for rendering. See http://mrbobby.r
                            eadthedocs.org/en/latest/userguide.html#usage for a
                            guide to template syntax

    optional arguments:
      -h, --help            show this help message and exit
      -O TARGET_DIRECTORY, --target-directory TARGET_DIRECTORY
                            Where to output rendered structure. Defaults to
                            current directory
      -v, --verbose         Print more output for debugging
      -c CONFIG, --config CONFIG
                            Configuration file to specify either [mr.bobby] or
                            [variables] sections
      -V, --version         Display version number
      -l, --list-questions  List all questions needed for the template
      -w, --remember-answers
                            Remember answers to .mrbobby.ini file inside output
                            directory
      -n, --non-interactive
                            Don't prompt for input. Fail if questions are required
                            but not answered
      -q, --quiet           Suppress all but necessary output
      -r RDR_FNAME_PLUGIN_TARGET, --rdr-fname-plugin-target RDR_FNAME_PLUGIN_TARGET
                            Specify target plugin like 10|20

By default, the target directory is the current folder. The most basic use case is rendering a template from a relative folder::

    $ mrbobby ../template_folder/

Or from a package::

    $ mrbobby some.package:template_folder/

Or from a zip file::

    $ mrbobby https://github.com/jpcw/mr.bobby/zipball/master

Or from a relative path in a zip file::

    $ mrbobby https://github.com/jpcw/mr.bobby/zipball/master#mrbobby/template_sample


Sample template to try out
--------------------------

::

    $ mrbobby mrbobby:template_sample/
    Welcome to mr.bobby interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Value in square brackets at the end of the questions present default value if there is no answer.


    --> How old are you? [24]: 

    --> What is your name?: Foobar

    --> Enter password: 


    Generated file structure at /current/directory/


Listing all questions needed to have corresponding variable for a template
--------------------------------------------------------------------------

::

    $ mrbobby --list-questions mrbobby:template_sample/
    author.age.default = 24
    author.age.help = We need your age information to render the template
    author.age.question = How old are you?
    author.name.question = What is your name?
    author.name.required = True
    author.password.command_prompt = getpass:getpass
    author.password.question = Enter password


Remember answers to a config file
------------------------------------

Running::

    $ mrbobby --remember-answers -O new_dir mrbobby:template_sample/
    ...

When everything is done, all answers are stored in **new_dir/.mrbobby.ini**
so later you reuse them::

    $ mrbobby --config new_dir/.mrbobby.ini -O new_dir another_template/
    ...


Using ``non-interactive`` mode
--------------------------------

Sometimes you might want to automate a script and use ``mrbobby``. It
is wise to tell ``mrbobby`` to not prompt for any input. ``mrbobby`` will use
given answers and defaults if answers are missing. In case a question
is required and doesn't have a default, error will be thrown.

Configuration
-------------

Configuration is done with ``.ini`` style files. There are two sections for configuration: :term:``mr.bobby`` and :term:``variables``.

Example of global config file ``~/.mrbobby`` or command line parameter ``mrbobby --config foo.ini``.

.. code-block:: ini

    [mr.bobby]
    verbose = True

    [variables]
    author.name = Jean-Philippe Camguilhem
    author.email = domen@dev.si

Specifying answers
******************

To answer some questions from a config file instead of interactively. Given ``me.ini``:

.. code-block:: ini

    [variables]
    author.name = Jean-Philippe Camguilhem
    author.email = domen@dev.si
    author.age = 24

do::

  $ mrbobby --config me.ini mrbobby:template_sample/

Specifying defaults
*******************

Sometimes you might want to override defaults for a template. Given ``me.ini``:

.. code-block:: ini

    [defaults]
    author.name = Jean-Philippe Camguilhem
    author.email = domen@dev.si
    author.age = 24

do::

  $ mrbobby --config me.ini mrbobby:template_sample/

``mrbobby`` will as you questions but default values will be also taken from config file.


Remote configuration
********************

Config file can also be loaded from a remote location::

  $ mrbobby --config https://raw.github.com/jpcw/mr.bobby/master/mrbobby/tests/example.ini mrbobby:template_sample/


Configuration inheritance
*************************

Configuration can be specified in multiple ways. See flow of mr.bobby on the documentation front page to know how options are preferred.


Nesting variables into namespaces called groups
***********************************************

All variables can be specified in namespaces, such as ``author.name``. Currently namespaces
don't do anything special besides providing readability.



``mr.bobby`` section reference
****************************

================  ===============================  =======================================================================
  Parameter         Default                          Explanation
================  ===============================  =======================================================================
ignored_files     No patterns                      Multiple Unix-style patterns to specify which files should be ignored:
                                                   for instance, to ignore, Vim swap files, specify ``*.swp``
non_interactive   False                            Don't prompt for input. Fail if questions are required but not answered
quiet             False                            Don't output anything except necessary
remember_answers  False                            Write answers to ``.mrbobby.ini`` file inside output directory
verbose           False                            Output more information, useful for debugging
================  ===============================  =======================================================================



Collection of community managed templates
-----------------------------------------

You are encouraged to use the ``bobbytemplates.something`` Python egg namespace to write
templates and contribute them to this list by making a `pull request <https://github.com/jpcw/mr.bobby>`_.

- `bobbytemplates.ielectric <https://github.com/jpcw/bobbytemplates.ielectric>`_
- `bobbytemplates.kotti <https://github.com/Kotti/bobbytemplates.kotti>`_
- `bobbytemplates.niteoweb <https://github.com/niteoweb/bobbytemplates.niteoweb>`_


Collection of community plugins
-------------------------------

You are encouraged to use the ``bobbyplugins.something`` Python egg namespace to write
templates and contribute them to this list by making a `pull request <https://github.com/jpcw/mr.bobby>`_.

- `bobbyplugins.jpcw <https://github.com/jpcw/bobbyplugins.jpcw>`_