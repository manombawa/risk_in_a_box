"""
Disaster risk assessment tool developed by AusAid and World Bank
- **GUI Test Cases.**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.0.1'
__date__ = '21/02/2011'
__copyright__ = ('Copyright 2012, Australia Indonesia Facility for '
                 'Disaster Reduction')

import sys
import unittest
# Needed though not used below
from PyQt4.QtGui import QApplication
from utilities_test import getQgisTestApp
QGISAPP, CANVAS, IFACE, PARENT = getQgisTestApp()

from riabhelp import RiabHelp


class RiabHelpTest(unittest.TestCase):
    """Test the risk in a box help GUI
    .. note:: Currently these tests will all fail unless you comment out the
    APP.exec_() lines because the web view does not load content without
    the main application event loop running.
    """
    def XtestDialogLoads(self):
        """Basic test to ensure the keyword dialog has loaded"""

        myHelp = RiabHelp(PARENT)
        #myHelp.show()
        #QGISAPP.exec_()

        myText = myHelp.ui.webView.page().currentFrame().toPlainText()
        myHelp.close()
        myExpectedText = 'This is the project: Risk in a Box - QGIS'
        myMessage = ('Expected to find "%s" in \n\n"%s"'
                     % (myExpectedText, myText))
        assert myText.contains(myExpectedText), myMessage

    def XtestDockHelp(self):
        """Test help dialog works with context set to 'dock'"""
        myHelp = RiabHelp(PARENT, theContext='dock')
        myText = myHelp.ui.webView.page().currentFrame().toPlainText()
        myExpectedText = 'Using the Risk in a Box Plugin'
        myMessage = ('Expected to find "%s" in \n\n"%s"'
                     % (myExpectedText, myText))
        assert myText.contains(myExpectedText), myMessage

    def XtestKeywordsHelp(self):
        """Test help dialog works with context set to 'keywords'"""
        myHelp = RiabHelp(PARENT, theContext='keywords')
        myText = myHelp.ui.webView.page().currentFrame().toPlainText()
        myExpectedText = 'avoid using spaces'
        myMessage = ('Expected to find "%s" in \n\n"%s"'
                     % (myExpectedText, myText))
        assert myText.contains(myExpectedText), myMessage

if __name__ == '__main__':
    suite = unittest.makeSuite(RiabHelpTest, 'test')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
