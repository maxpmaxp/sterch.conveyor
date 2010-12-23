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
    
class IWorkerBase(IThread,
                  IEventMixin,
                  IDelayMixin):
    """ Wroker base interface """
    event = Object(title=u"Event to stop worker", schema=IEvent, requred=True, readonly=True)
    
    def activity(*args, **kwargs):
        """ Main worker activity. 
            MUST be generator.  """

class IFirstWorker(IWorkerBase, IOutQueueMixin):
    """ First worker that creates initial tasks queue """
    
    def activity():
        """ Activity have no input args. This is initial tasks generator. """
    
class ILastWorker(IWorkerBase, IInQueueMixin):
    """ Last worker that processes last tasks que queue """

class IWorker(IWorkerBase, IInQueueMixin, IOutQueueMixin):
    """ Regular worker. It gets tasks from input queue and puts to output queue """
    
class IGroup(ISequence):
    """ Sequence of workers """
    
    def start_all():
        """" start all workers """
    
    def stop_all():
        """" notify all workers to stop """
    
    def filter_dead_workers():
        """ removes dead workers from sequence """
        
    def live_count():
        """ number of active workers """

class IStageBase(Interface, IEventMixin, IDelayMixin):
    """ Data processing stage """
    event = Object(title=u"Event to stop all stage workers", schema=IEvent, requred=True, readonly=True)
    name = TextLine(title=u"Stage name", required=True, readonly=True)
    group = Object(title=u"Group of workers", required=True, readonly=True)
     
class IInitialStage(IStageBase, IOutQueueMixin):
    """ Initial data processing stage """

class IFinalStage(IStageBase, IInQueueMixin):
    """ Final data processing stage """

class IStage(IStageBase, IInQueueMixin, IOutQueueMixin):
    """ Regular data processing stage. Requires both input and output queues """
    order = Int(title=u"Delay in sec. between activity cycles", 
                required=True,
                readonly=True)
    
class IConveyor(IThread, IEventMixin):
    """ Conveyor of parallel data processing.
        When starts it MUST start all stages' workers
    """
    
    stages = Tuple(title=u"All stages ordered.", readonly=True, required=True)
    
    def stop_all():
        """ Fires events to stop all stages """