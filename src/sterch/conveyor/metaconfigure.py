### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################

"""Metadirectives implementations for the ZTK based sterch.threading package

"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL" 

from interfaces import IFirstWorker, ILastWorker, IRegularWorker
from zope.component import createObject, getUtility
from zope.component.interfaces import IFactory 
from zope.configuration.exceptions import ConfigurationError

class Conveyor(object):
    """ Conveyor directive handler """
    
    def __init__(self, _context, name):
        self._context = _context
        self.name = name
        self.init_stage = False
        self.final_stage = False
        self.stages = []
        
    def init_stage(self, _context, **kwargs):
        """ init_stage subdirective processing """
        self.init_stage = kwargs
        
        
    def final_stage(self, _context, **kwargs):
        """ final_stage subdirective processing """
        self.final_stage = kwargs
        
    def stage(self, _context, **kwargs):
        """ stage subdirective procesing """
        self.stages.append(kwargs)
        
    def __call__(self):
        """ whole directive processing  """
        if not self.init_stage: raise ConfigurationError(u"No initial stage defined")
        if not self.final_stage: raise ConfigurationError(u"No final stage defined")
        # trying to build conveyor chain
        ordered_stages = [self.init_stage]
        curq = self.init_stage['out_queue']
        in_queues = []
        out_queues = [cur_queue]
        while self.stages:
            s = self.stages.pop()
            if s.in_queue in in_queues: raise ConfigurationError(u"Input queue could be used only in one stage.")
            if s.out_queue in out_queues: raise ConfigurationError(u"Output queue could be used only in one stage.")
            if s.in_queue == curq:
                ordered_stages.append(s)
                curq = s.out_queue
                in_queues.append(s.in_queue)
                out_queues.append(s.out_queue)
            else:
                self.stages = [s,] + self.stages
        if stages: ConfigurationError(u"There are dummy stages within the conveyor")
        if stages[:-1]['out_queue'] != self.final_stage['in_queue']:
            ConfigurationError(u"Conveyor must be finished with final_stage.")            
        stages.append(self.final_stage)
        # constructing the conveyor
        __stages = [] 
        # 1st stage
        s = stages[0]
        s['event'] = s['event'] if s.get('event') else createObject('sterch.threading.Event')
        stages = stages[1:]
        __stages.append(createObject('sterch.conveyor.FirstStage', **s))
        # middle stages
        for s in stages[:-1]:
            s['event'] = s['event'] if s.get('event') else createObject('sterch.threading.Event')
            __stages.append(createObject('sterch.conveyor.RegularStage', **s))
        #last stage
        s = stages[:-1]
        s['event'] = s['event'] if s.get('event') else createObject('sterch.threading.Event')
        __stages.append(createObject('sterch.conveyor.FinalStage', **s))
        conveyor = createObject('sterch.conveyor.Conveyor', self.name, __stages)
        self._context.action(
            discriminator = ('utility', IConveyor, self.name),
            callable = handler,
            args = ('registerUtility', conveyor, IConveyor, self.name)
        )