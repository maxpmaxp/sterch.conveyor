### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2010
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2010
#######################################################################
"""Interfaces for the ZTK based sterch.worker package

"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL" 

from sterch.queue.interfaces import IQueue
from sterch.threading.interfaces import IThread, IEvent
from zope.interface import Interface
from zope.interface.common.sequence import ISequence
from zope.schema import Object, Int, Tuple

class IEventMixin(Interface):
    event = Object(title=u"Event", schema=IEvent, requred=True, readonly=True)
    
class IDelayMixin(Interface):
    delay = Int(title=u"Delay in sec. between activity cycles", min=0, default=0, required=True, readonly=True)
    
class IOutQueueMixin(Interface):
    out_queue = Object(title=u"Queue to put tasks", schema=IQueue, readonly=True, required=True)

class IInQueueMixin(Interface):
    in_queue = Object(title=u"Queue to get tasks", schema=IQueue, readonly=True, required=True)
    
class IWorker(IThread,
                  IEventMixin,
                  IDelayMixin):
    """ Wroker base interface """
    event = Object(title=u"Event to stop worker", schema=IEvent, requred=True, readonly=True)
    
    def activity(*args, **kwargs):
        """ Main worker activity. 
            MUST be generator.  """

class IFirstWorker(IWorker, IOutQueueMixin):
    """ First worker that creates initial tasks queue """
    
    def activity():
        """ Activity have no input args. This is initial tasks generator. """
    
class ILastWorker(IWorker, IInQueueMixin):
    """ Last worker that processes last tasks que queue """

class IRegularWorker(IWorker, IInQueueMixin, IOutQueueMixin):
    """ Regular worker. It gets tasks from input queue and puts to output queue """

class IDelayedFinish(Interface):
    """ Interface of delayed finish.
        It describes situation when stopping is parallel task 
        and may take a lot of time.
    """
    def stop():
        """ Do something to stop (f.e. fire event) """
        
    def is_finished():
        """ Check was it really finished """
        
class IGroup(ISequence, IDelayedFinish):
    """ Sequence of workers """
    name = TextLine(title=u"Group name", required=True, readonly=True)
    
    def start():
        """" start all workers """
    
    def filter_dead_workers():
        """ removes dead workers from sequence """
        
    def live_count():
        """ number of active workers """

class IStage(IDelayedFinish, IEventMixin, IDelayMixin):
    """ Data processing stage """
    name = TextLine(title=u"Stage name", required=True, readonly=True)
    
    def has_tasks():
        """ Returns True if stage has unfinished tasks finished, False otherwise. """
    
    def start():
        """ starts stage """
            
class IInitialStage(IStage, IOutQueueMixin):
    """ Initial data processing stage """

class IFinalStage(IStage, IInQueueMixin):
    """ Final data processing stage """

class IRegularStage(IStage, IInQueueMixin, IOutQueueMixin):
    """ Regular data processing stage. Requires both input and output queues """
    order = Int(title=u"Delay in sec. between activity cycles", 
                required=True,
                readonly=True)
    
class IConveyor(IThread, IDelayMixin):
    """ Conveyor of parallel data processing.
        When starts it MUST start all stages' workers
    """
    stages = Tuple(title=u"All stages ordered.", readonly=True, required=True)