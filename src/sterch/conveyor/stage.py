### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2010
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2010
#######################################################################

""" data processing stage
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

from assistance import InQueueMixIn
from group import Group
from interfaces import IGroup, IRegularStage, IFirstStage, ILastStage
from zope.interface import implements
from zope.component import getUtility
from zope.component.interfaces import IFactory

class StageBase(object):
    """ Base data processing stage.
        This class DOES NOT implemet IStage.
        There is no way to implement has_tasks
    """
        
    def __init__(self, name, group):
        """  
            name --- stage name
            group --- worker's group
        """
        self._name = name
        self.group = group   
               
    @property
    def name(self):
        """ name must be read only according to IStage """
        return self._name
    
    def start(self):
        """ Start stage """
        self.group.start_all()
        
    def stop(self):
        """ Tries to stop stage """
        self.group.stop_all()
        
    def is_finished(self):
        """ Checks does group of workers finish its activity """
        self.group.filter_dead_workers()
        return len(self.group) == 0
    
    def has_tasks(self):
        """ Must be implemented in descendants """
        raise NotImplementedError("Not implemented yet.")
    
class FirstStage(StageBase):
    """ First data processing stage. 
        Initial tasks generation.
    """
    implements(IFirstStage)
    
    def __init__(self, name, qty, out_queue, event, delay, activity):
        """ 
            name --- stage name
            qty --- number of workers to process stage
            out_queue --- queue to put tasks
            event --- event to stop all workers
            delay --- processing delay
            activity --- callable represents stage activity 
        """
        w_factory = getUtility(IFacoty, name="sterch.conveyor.FirstWorker") 
        g_factory = getUtility(IFacoty, name="sterch.conveyor.Group")
        w_args = (out_queue, event, delay, activity)
        group = g_factory(qty, w_factory, *w_args)
        StageBase.__init__(self, name, group)
        
    def has_tasks(self):
        """ Initial stage has no unfinished tasks."""
        return False
    
class LastStage(StageBase, InQueueMixin):
    """ Last data processing stage. 
        Results generation.
    """
    implements(ILastStage)
    
    def __init__(self, name, qty, in_queue, event, delay, activity):
        """ 
            name --- stage name
            qty --- number of workers to process stage
            in_queue --- queue to get tasks
            event --- event to stop all workers
            delay --- processing delay
            activity --- callable represents stage activity 
        """
        w_factory = getUtility(IFacoty, name="sterch.conveyor.LastWorker") 
        g_factory = getUtility(IFacoty, name="sterch.conveyor.Group")
        w_args = (in_queue, event, delay, activity)
        group = g_factory(qty, w_factory, *w_args)
        StageBase.__init__(self, name, group)


class RegularStage(StageBase, InQueueMixin):
    """ Regular data processing stage. 
        Take tasks from input queue and put next tasks to output queue.
    """
    implements(IRegularStage)
    def __init__(self, name, order, qty, in_queue, out_queue, event, delay, activity):
        """ 
            name --- stage name
            order --- stage number in data processing flow. Used to order stages
            qty --- number of workers to process stage
            in_queue --- queue to get tasks
            out_queue --- queue to put next tasks
            event --- event to stop all workers
            delay --- processing delay
            activity --- callable represents stage activity 
        """
        self._order = order
        w_factory = getUtility(IFacoty, name="sterch.conveyor.RegularWorker") 
        g_factory = getUtility(IFacoty, name="sterch.conveyor.Group")
        w_args = (in_queue, event, delay, activity)
        group = g_factory(qty, w_factory, *w_args)
        StageBase.__init__(self, name, group)
    
    @propery
    def order(self):
        """ This is Read Only attribute according to IRegularStage"""
        return self._order