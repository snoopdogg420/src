from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from toontown.chat.ChatGlobals import WTSystem
from toontown.chat.WhisperPopup import WhisperPopup
from otp.otpbase import OTPGlobals


class DistributedEvent(DistributedObject, FSM):
    notify = directNotify.newCategory('DistributedEvent')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, self.__class__.__name__)

    def start(self):
        pass

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        self.cr.event = self
        self.joinEvent()

    def delete(self):
        self.cr.event = None

        DistributedObject.delete(self)

    def messageParticipants(self, message):
        whisper = WhisperPopup(message, OTPGlobals.getInterfaceFont(), WTSystem)
        whisper.manage(base.marginManager)

    def joinEvent(self):
        self.sendUpdate('joinEvent', [base.localAvatar.doId])

    def leaveEvent(self):
        self.sendUpdate('leaveEvent', [base.localAvatar.doId])

    def setState(self, state, timestamp):
        self.request(state, timestamp)
