from direct.distributed.DistributedObject import DistributedObject
from toontown.chat.ChatGlobals import WTSystem
from toontown.chat.WhisperPopup import WhisperPopup
from otp.otpbase import OTPGlobals


class DistributedEvent(DistributedObject):
    notify = directNotify.newCategory('DistributedEvent')

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
