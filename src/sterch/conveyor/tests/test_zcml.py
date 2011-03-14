### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2010
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2010
#######################################################################

""" Base test classes for sterch.conveyor
"""
__author__  = "Maxim Polscha (maxp@sterch.net)"
__license__ = "ZPL" 

from setup import TestSetup

class Test(TestSetup):
    """Test the various zcml configurations"""
    
    def test_correct_zcml_no_events(self):
        pass
    
    def test_correct_zcml_with_events(self):
        pass
    
    def test_2stages_only(self):
        pass
    
    def test_loop(self):
        pass
    
    def test_no_init_stage(self):
        pass
     
    def test_no_2nd_stage(self):
        pass
    
    def test_no_final_stage(self):
        pass
    
    def test_final_stage_unreachable(self):
        pass
    
    def test_dummy_stages(self):
        pass