from direct.distributed.DistributedObject import DistributedObject
from toontown.chat.ChatGlobals import WTSystem
from toontown.chat.WhisperPopup import WhisperPopup
from otp.otpbase import OTPGlobals


class DistributedEvent(DistributedObject):
    notify = directNotify.newCategory('DistributedEvent')

    def start(self):
        pass

    def announceGenerate(self):
        self.cr.event = self

    def delete(self):
        self.cr.event = None

    def messageParticipants(self, message):
        whisper = WhisperPopup(message, OTPGlobals.getInterfaceFont(), WTSystem)
        whisper.manage(base.marginManager)
