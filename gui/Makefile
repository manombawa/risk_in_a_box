#/***************************************************************************
# Riab
#
# Disaster risk assessment tool developed by AusAid and World Bank
#                             -------------------
#        begin                : 2012-01-09
#        copyright            : (C) 2012 by Australia Indonesia Facility for Disaster Reduction
#        email                : ole.moller.nielsen@gmail.com
# ***************************************************************************/
#
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

# Makefile for a PyQGIS plugin

PLUGINNAME = riab

PY_FILES = riab.py riabdock.py riabhelp.py __init__.py

EXTRAS = icon.png

UI_FILES = ui_riabdock.py \
					 ui_riabhelp.py \
					 riabkeywordsdialogbase.py

RESOURCE_FILES = resources.py

default: compile

compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@  $<
	@#this is ugly but the resource referenced by the ui
	@#looks for a file generated with a different name
	cp resources.py resources_rc.py

clean: compile
	rm $(UI_FILES)

%.py : %.ui
	pyuic4 -o $@ $<

# Run the test suite followed by pep8 style checking
test: test_suite pep8

# Run pep8 style checking only
pep8: compile
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	pep8 --repeat --ignore=E203 --exclude ui_riabhelp.py,ui_riab.py,ui_riabdock.py,resources.py,resources_rc.py .

# Run test suite only
test_suite: compile
	@echo "----------------------"
	@echo "Regresssion Test Suite"
	@echo "----------------------"

	@# Preceding dash means that make will continue in case of errors
	-nosetests -v --with-id --with-coverage --cover-package=.

indent:
	@# sudo apt-get install python2.7-examples for reindent script
	python /usr/share/doc/python2.7/examples/Tools/scripts/reindent.py *.py
