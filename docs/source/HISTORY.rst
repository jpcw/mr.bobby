Changelog
=========


0.1a10 (unreleased)
-------------------

- add entry_points plugins support for render_filename
  [Jean-Philippe Camguilhem]

- move exceptions to bobbyexceptions
  [Jean-Philippe Camguilhem]

- Use jinja2 < 2.7, since 2.7+ doesn't support Python 3.2

- Filename variable name substitution regex failed to compile on windows
  [Jean-Philippe Camguilhem]

- Do not copy ``.DS_Store``.
  [Godefroid Chapelle]

- Configure patterns of files to ignore through
  ``ignored_files`` option of ``mr.bobby`` section.
  [Godefroid Chapelle]


0.1a9 (2013-04-26)
------------------

- Regex to detect variable names when rendering file names was broken when 
  directory path contains pluses.
  [Godefroid Chapelle]


0.1a8 (2013-03-11)
------------------

- Depend on six>=1.2.0
  [Jean-Philippe Camguilhem]

- Moved all exceptions to `mrbobby.exceptions` module
  [Jean-Philippe Camguilhem]

- Fix loading of zip files
  [Jean-Philippe Camguilhem]

- #28: Remote loading of config files
  [Nejc Zupan]

- #30: Keep newlines of rendered template
  [Jean-Philippe Camguilhem]


0.1a7 (2013-01-23)
------------------

- Don't depend on argparse in python 2.7 and higher, since it's already
  in stdlib
  [Jean-Philippe Camguilhem]

- #22: Prevent users from specifying target directory inside template dir
  [Jean-Philippe Camguilhem]


0.1a6 (2013-01-02)
------------------

- Use ``StrictUndefined`` with jinja2 renderer so that any missing key is
  reported as an error
  [Jean-Philippe Camguilhem]

- If a key in a namespace was missing while rendering, no error was raised
  [Jean-Philippe Camguilhem]

- Added hook ``mrbobby.hooks.show_message``
  [Jean-Philippe Camguilhem]

- ``mrbobby.validators.boolean`` renamed to ``mrbobby.hooks.to_boolean``
  [Jean-Philippe Camguilhem]

- Renamed ``validators.py`` to ``hooks.py``
  [Jean-Philippe Camguilhem]

- Removed ``validators`` and ``action`` settings from ``[questions]`` as it is
  superseded by hooks
  [Jean-Philippe Camguilhem]

- Added ``pre_ask_question`` and ``post_ask_question`` to ``[questions]`` section
  [Jean-Philippe Camguilhem]
  
- Added ``pre_render``, ``post_render`` and  ``post_render_msg`` options
  [Jean-Philippe Camguilhem]

- Added ``[defaults]`` section that will override template defaults. The only
  difference to ``[variables]`` is that variables provide default answers
  [Jean-Philippe Camguilhem]

- Moved ``renderer`` parameter to ``[template]`` section
  [Jean-Philippe Camguilhem]

- Added ``[template]`` section that is parsed only from ``.mrbobby.ini`` inside a
  template directory.
  [Jean-Philippe Camguilhem]

- Correctly evaluate boolean of ``quiet`` and ``verbose`` settings
  [Jean-Philippe Camguilhem]

- Added ``non_interactive`` setting that will not prompt for any input and fail
  if any of required questions are not answered
  [Jean-Philippe Camguilhem]

- Added ``remember_answers`` setting that will create ``.mrbobby.ini`` file inside
  rendered directory with all the answers written to ``[variables]`` section
  [Jean-Philippe Camguilhem]

- Include changelog in documentation
  [Jean-Philippe Camguilhem]

- ``Question`` does no longer raise error if unknown parameter is passed from a
  config file. Instead those parameters are saved to ``question.extra`` that can
  be later inspected and validated. This is first step to have advanced question
  types such as question with a set of predefined answers
  [Jean-Philippe Camguilhem]

- Rewrite all py.test stuff to nosetests, so we have unified testing now. This
  also fixes flake8 segfaults on pypy
  [Jean-Philippe Camguilhem]


0.1a5 (2012-12-12)
------------------

- #26: Variables were not correctly parsed from config files
  [Jean-Philippe Camguilhem]


0.1a4 (2012-12-11)
------------------

- Fix MANIFEST.in so that template examples are also included with distribution
  [Jean-Philippe Camguilhem]

- Add -q/--quiet option to suppress output which isn't strictly necessary
  [Sasha Hart]

- Suppress the interactive-mode welcome banner if there are no questions to ask
  [Sasha Hart]

- Don't raise KeyError: 'questions_order' if [questions] is missing in an ini
  [Sasha Hart]


0.1a3 (2012-11-30)
------------------

- #13: Read user config from ~/.mrbobby (as stated in docs and inline comments).
  [Andreas Kaiser]


0.1a2 (2012-11-29)
------------------

- #12: Fix unicode errors when using non-ASCII in questions or defaults
  [Jean-Philippe Camguilhem]

- Ask questions in same order they were
  defined in template configuration file
  [Jean-Philippe Camguilhem]


0.1a1 (2012-10-19)
------------------

- Initial release.
  [Jean-Philippe Camguilhem, Cyprien Le Pannérer]