Lettuce Stub Methods Generator
=============================

* Provide stories as command line arguments:

``loaf test1.test test2.test test3.test``

and get your stubs:

test1.py test2.py test3.py


* Or in 1 file:

``loaf test1.test test2.test --to __init__.py``


* Or with different prepositions:

``loaf --prepositions=When,Then,And,Require test1.test``

* Or with different imports:

``loaf --imports imports_template test1.test``


Sample:
======

* For feature:

::

	Feature: Monday feature
	Scenario: Typical Monday Scenario
	Wherever I go "home"
	Always I return at "work"


* We get stubs:

::

	from lettuce import step

	
	@step(u'I go "([^"]*)"')
	def whethever_i_go_group1(step, group1):
	    pass
	
	@step(u'I return at "([^"]*)"')
	def always_i_return_at_group1(step, group1):
	    pass


* By using command:

``loaf --prepositions Wherever,Always test1.test``

