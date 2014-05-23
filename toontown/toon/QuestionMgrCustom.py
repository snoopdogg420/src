import random


class QuestionMgr:
    
    def __init__(self):
        self.greetings = ['hi', 'hello', 'hey', 'sup', 'howdy', 'yo']
        self.greetingResp = ['Hello there, ', 'Howdy there, ', 'Hows it hanging, ', 'How do you do, ', 'Whats up, ', 'Woah! You scared me there ']
        self.response = ''
        self.confused = 1
        
    def ask(self, message, sender):
        msg = message.lower()
        vbls = msg.split()
        for i in xrange(0, len(vbls)):
            if vbls[i] in self.greetings:
                index = random.randint(0, len(self.greetingResp) -1)
                helloResp = self.greetingResp[index]
                respFinal = helloResp + '%s' % sender + '!'
                self.response += helloResp
                self.confused = 0
        else:
            if self.confused:
                self.response += 'Dang, I really don\'t understand you.'
        self.confused = 1
        return self.response
