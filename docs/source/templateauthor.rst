Writing your own template
=========================


Starting
--------

Writing your own template is as easy as creating a `.mrbobby.ini` that may contain questions.
Everything else is extra. To start quickly, use the template starter that ships with `mr.bobby`::

  $ mrbobby mrbobby:template_starter/
  Welcome to mr.bobby interactive mode. Before we generate directory structure, some questions need to be answered.

  Answer with a question mark to display help.
  Value in square brackets at the end of the questions present default value if there is no answer.


  --> How old are you? [24]:

  --> What is your name?: Foobar

  --> Enter password:


  Generated file structure at /home/ielectric/code/mr.bobby

See `.mrbobby.ini` for sample questions and `sample.txt.bobby` for sample rendering.


How it works
------------

Files inside the structure can be just copied to destination, or they can be suffixed with `.bobby` and the templating engine
will be used to render them.

By default a slightly customized `Jinja2` templating is used. The big differences are that variables are referenced with `{{{ variable }}}` instead of `{{ variable }}` and blocks are `{{% if variable %}}` instead of `{% if variable %}`. To read more about templating see `Jinja2 documentation <http://jinja.pocoo.org/docs/templates/#variables>`_.

Variables can also be used on folder and file names. Surround variables with plus signs. For example `foo/+author+/+age+.bobby` given variables *author* being `Foo` and *age* being `12`, `foo/Foo/12` will be rendered.

Templating engine can be changed by specifying `renderer` in mr.bobby config section in :term:`dotted notation`. It must be a callable that expects a text source as the first parameter and a dictionary of variables as the second.

When rendering the structure, permissions will be preserved for files.


Writing Questions
-----------------

`[question]` section in `.mrbobby.ini` specifies a *schema* for how `[variables]` are validated.
Example speaks for itself:

.. code-block:: ini

  [questions]
  author.name.question = What is your name?
  author.name.required = True

  author.age.question = How old are you?
  author.age.help = We need your age information to render the template
  author.age.default = 24

  author.password.question = Enter password
  author.password.command_prompt = getpass:getpass

Questions will be asked in the order written in `.mrbobby.ini`.


``questions`` section reference
*******************************


================== ================= =================================================================================================
  Parameter          Default           Explanation
================== ================= =================================================================================================
name                                 Required. Unique identifier for the question
question                             Required. Question given interactively to a user when generating structure
default            None              Default value when no answer is given. Can be a `dotted notation`
required           False             Specify if question must be answered
command_prompt     :func:`raw_input` Function that accepts a question and asks user for the answer
help               ""                Extra help returned when user inputs a question mark
pre_ask_question   None              :term:`dotted notation` function to run before asking the question
post_ask_question  None              :term:`dotted notation` function to run after asking the question (also does validation)
================== ================= =================================================================================================

Common needs for templating
---------------------------

Default value of the question is dynamic
****************************************

Use something like:

.. code-block:: ini

    [questions]
    author.name.question = What's your name?
    author.name.pre_ask_question = bobbytemplates.mytemplate.hooks:pre_author

Where `pre_author` function will modify the question and provide new :attr:`mrbobby.configurator.Question.default`.

Conditionally render a file
***************************

Use something like:

.. code-block:: ini

    [template]
    post_render = bobbytemplates.mytemplate.hooks:delete_readme

And based on `mrbobby.Configurator.variables` answers, delete a file or add one.


Based on the answer of the question do something
************************************************

Use something like:

.. code-block:: ini

    [questions]
    author.name.question = What's your name?
    author.name.post_ask_question = bobbytemplates.mytemplate.hooks:post_author

Where `post_author` function will take :class:`mrbobby.configurator.Configurator`, question and it's answer. 

Ask a question based on answer of previous question
***************************************************

use post_ask_question and add another question (is that possible if we are looping through questions? -> While questions: questions.pop())


Hooks
-----

A list of places where you can hook into the process flow and provide your
custom code. All hooks can have multiple entries limited by whitespace.

.. _post-render-hook:

Post render hook
****************

If you would like to execute a custom Python script after rendering
is complete, you can use `post_render` hook in your ``.mrbobby.ini``.

.. code-block:: ini

    [template]
    post_render = bobbytemplates.mytemplate.hooks:my_post_render_function

This assumes you have a `bobbytemplate.mytemplate` egg with a ``hooks.py``
module. This module contains a ``my_post_render_hook`` function, which gets
called after mr.bobby has finished rendering your template.

The function expects one argument (:class:`mrbobby.configurator.Configurator`)
and looks something like this:

.. code-block:: python

    def my_post_render_function(configurator):
        if configurator.variables['author.email']:
            # do something here

.. _pre-render-hook:

Pre render hook
***************

Much like the :ref:`post-render-hook` example above, you can use ``pre_render``
variable in your ``.mrbobby.ini`` to specify a function to call before rendering
starts.

.. code-block:: ini

    [template]
    pre_render = bobbytemplates.mytemplate.hooks:my_pre_render_function


.. _pre-question-hook:

Pre question hook
*****************

For maximum flexibility, `mr.bobby` allows you to set hooks to questions. Using
``pre_ask_question`` in your ``.mrbobby.ini`` allows you to run custom
code before a certain question.

The function expects two arguments:
 * :class:`mrbobby.configurator.Question`
 * :class:`mrbobby.configurator.Configurator`

.. code-block:: ini

    [questions]
    author.name.question = What's your name?
    author.name.pre_ask_question = bobbytemplates.mytemplate.hooks:pre_author

.. code-block:: python

    def set_fullname(configurator, question):
        question.default = 'foobar'

If you want question to be skipped, simply raise :exc:`mrbobby.bobbyexceptions.SkipQuestion` inside
your hook.

.. _post-question-hook:

Post question hook
******************

Similar to :ref:`pre-question-hook` example above, you can use
``post_ask_question`` variable in your ``.mrbobby.ini`` to specify a function to
call after a question has been asked. :ref:`post-question-hook` **must** return
the answer of the question.

The function expects three arguments:
 * :class:`mrbobby.configurator.Question`
 * :class:`mrbobby.configurator.Configurator`
 * answer from the question

.. code-block:: ini

    [questions]
    author.firstname.question = What's your name?
    author.lastname.question = What's your surname?
    author.lastname.post_ask_question = bobbytemplates.mytemplate.hooks:set_fullname

.. code-block:: python

    def set_fullname(configurator, question, answer):
        configurator.variables['author.fullname'] =
            configurator.variables['author.firstname'] + ' ' +
            answer
        return answer

Raise :exc:`mrbobby.bobbyexceptions.ValidationError` to re-ask the question.


Hooks shipped with `mr.bobby`
***************************

See :mod:`mrbobby.hooks`.


``template`` section reference
------------------------------

===================== =============================== ======================================================================================
Parameter             Default                         Explanation
===================== =============================== ======================================================================================
renderer              mrbobby.rendering:jinja2_renderer Function for rendering templates in :term:`dotted notation`
pre_render            None                            :term:`dotted notation` function to run before rendering the templates
post_render           None                            :term:`dotted notation` function to run after rendering the templates
===================== =============================== ======================================================================================
