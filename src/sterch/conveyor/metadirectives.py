### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2010
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2010
#######################################################################

"""ZCML directives interfaces for the ZTK based sterch.conveyor package

"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

from sterch.threading.interfaces import IName
from zope.interface import Interface, invariant, Invalid
from zope.configuration.fields import GlobalObject
from zope.schema import TextLine, Int, Float
       
class IConveyorDirective(IName):
    """ <conveyor ...>  complex directive interface """
    
class IStageBase(IName):
    """ generic stage fields """
    activity = GlobalObject(title=u"Callable object to process tasks on the stage.",
                            constraint=lambda obj:hasattr(obj,'__call__'))
    quantity = Int(title=u"Number of workers for the stage.", min=0, required=True)
    delay = Int(title=u"Delay to wait tasks in queue (sec., 3 by default)", min=0, required=False, default=3)
    event = TextLine(title=u"IEvent utility name to stop workers.",
                     description=u"""Optional. If not defined event ill be created.
                                   Could be used for other tasks synchronization.""",
                     required=False)
            
class IInQueue(Interface):
    """ Input queue interface """
    in_queue = TextLine(title=u"IQueue utility name to be used as input tasks queue.", required=True) 
    
class IOutQueue(Interface):
    """ Output queue interface """
    out_queue = TextLine(title=u"IQueue utility name to be used as output tasks queue.", required=True)
    
class IInitStage(IStageBase, IOutQueue):
    """ Initial stage. Requires output queue only to put new tasks. """
    
class IFinalStage(IStageBase, IInQueue):
    """ Final stage. Requires input queue only to get tasks. """

class IStageDirective(IStageBase, IInQueue, IOutQueue):
    """ Regular stage. Requires both input and output queues. """      