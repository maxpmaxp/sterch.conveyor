### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2010
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2010
#######################################################################

""" Tests for IP address field
"""
__author__  = "Maxim Polscha (maxp@sterch.net)"
__license__ = "ZPL" 

import zcml

from setup import TestSetup
from sterch.conveyor.interfaces import IConveyor
from unittest import TestCase, makeSuite, main
from zope.component import queryUtility
from zope.configuration.xmlconfig import XMLConfig

class Test(TestSetup):
    """Test the various zcml configurations"""
    
    def test_correct_zcml_no_events(self):
        XMLConfig('valid_no_events.zcml', zcml)
        c = queryUtility(IConveyor, name="Test #1")
        self.assertTrue(c is not None)
                   
def test_suite():
    suite = makeSuite(Test)
    return suite

if __name__ == '__main__':
    main(defaultTest='test_suite')
