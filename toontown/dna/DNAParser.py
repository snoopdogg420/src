import libpandadna

from libpandadna.DNAAnimBuilding import DNAAnimBuilding
from libpandadna.DNAAnimProp import DNAAnimProp
from libpandadna.DNACornice import DNACornice
from libpandadna.DNADoor import DNADoor
from libpandadna.DNAFlatBuilding import DNAFlatBuilding
from libpandadna.DNAFlatDoor import DNAFlatDoor
from libpandadna.DNAGroup import DNAGroup
from libpandadna.DNAInteractiveProp import DNAInteractiveProp
from libpandadna.DNALandmarkBuilding import DNALandmarkBuilding
from libpandadna.DNANode import DNANode
from libpandadna.DNAProp import DNAProp
from libpandadna.DNASign import DNASign
from libpandadna.DNASignBaseline import DNASignBaseline
from libpandadna.DNASignGraphic import DNASignGraphic
from libpandadna.DNASignText import DNASignText
from libpandadna.DNAStreet import DNAStreet
from libpandadna.DNAVisGroup import DNAVisGroup
from libpandadna.DNAWall import DNAWall
from libpandadna.DNAWindows import DNAWindows

from libpandadna.DNAStorage import DNAStorage
from libpandadna.DNALoader import DNALoader

from libpandadna.DNASuitEdge import DNASuitEdge
from libpandadna.DNASuitPoint import DNASuitPoint
from libpandadna.DNASuitPath import DNASuitPath

from libpandadna.DNABattleCell import DNABattleCell

def loadDNAFile(*a, **kw):
    return loader.loadDNAFile(*a, **kw)
    
def loadDNAFileAI(*a, **kw):
    try:
        return simbase.air.loadDNAFileAI(*a, **kw)
        
    except:
        return loader.loadDNAFileAI(*a, **kw)
    
from pandac.PandaModules import *
def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
    doorNodePath.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
    doorNodePath.setColor(color, 0)
    
    leftHole = doorNodePath.find('door_*_hole_left')
    leftHole.setName('doorFrameHoleLeft')
    
    rightHole = doorNodePath.find('door_*_hole_right')
    rightHole.setName('doorFrameHoleRight')
    
    leftDoor = doorNodePath.find('door_*_left')
    leftDoor.setName('leftDoor')
    
    rightDoor = doorNodePath.find('door_*_right')
    rightDoor.setName('rightDoor')
    
    doorFlat = doorNodePath.find('door_*_flat')
    
    leftHole.wrtReparentTo(doorFlat, 0)
    rightHole.wrtReparentTo(doorFlat, 0)
    
    doorFlat.setEffect(DecalEffect.make())
    
    rightDoor.wrtReparentTo(parentNode, 0)
    leftDoor.wrtReparentTo(parentNode, 0)

    rightDoor.setColor(color, 0)
    leftDoor.setColor(color, 0)
    
    leftHole.setColor((0, 0, 0, 1), 0)
    rightHole.setColor((0, 0, 0, 1), 0)

    doorTrigger = doorNodePath.find('door_*_trigger')
    doorTrigger.setScale(2, 2, 2)
    doorTrigger.wrtReparentTo(parentNode, 0)
    doorTrigger.setName('door_trigger_' + block) 
