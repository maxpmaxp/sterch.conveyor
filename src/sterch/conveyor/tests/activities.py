### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2010
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2010
#######################################################################

""" Activities for test cass for sterch.conveyor
"""
__author__  = "Maxim Polscha (maxp@sterch.net)"
__license__ = "ZPL" 

from threading import Lock

gl_lock = Lock()
gl_jobs_counter = 0
gl_N = 50 

def increment(job): 
    job['value'] +=1
    yield job
    
def mul10(job): 
    job['value'] *=10
    yield job

def jobs():
    """ jobs generator. Generates tasks and expected results for the tests """
    global gl_N
    for i in xrange(1,10):
        yield dict(value = i, result = (i * 10 + 1))
        
def check_results(job):
    """ Check value against expected result """
    assert job['result'] == job['value']
    global gl_jobs_counter, gl_N, gl_lock
    with gl_lock: gl_jobs_counter +=1
    assert gl_jobs_counter <= gl_N