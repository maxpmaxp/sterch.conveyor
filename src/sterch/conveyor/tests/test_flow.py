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

from activities import get_jobs_counter, reset_jobs, gl_N, get_results
try:
    from queue import Empty
except ImportError:
    from Queue import Empty
from setup import TestSetup
from sterch.conveyor.interfaces import IConveyor
from unittest import TestCase, makeSuite, main
from zope.component import queryUtility
from zope.configuration.xmlconfig import XMLConfig

EXECUTION_TIME_LIMIT = 60

class Test(TestSetup):
    """Test the various zcml configurations"""
    
    def test_correct_zcml_no_events(self):
        XMLConfig('valid_no_events.zcml', zcml)()
        c = queryUtility(IConveyor, name="Test #1")
        self.assertTrue(c is not None)
        reset_jobs()
        c.start()
        c.join(EXECUTION_TIME_LIMIT)
        self.assertFalse(c.isAlive())
        q = get_results()
        self.assertEqual(q.qsize(), gl_N)
        self.assertEqual(get_jobs_counter(), gl_N)
        try:
            while True:
                task = q.get(False)
                self.assertEqual(task['value'], task['result'])
        except Empty:
            pass
                   
def test_suite():
    suite = makeSuite(Test)
    return suite

if __name__ == '__main__':
    main(defaultTest='test_suite')
