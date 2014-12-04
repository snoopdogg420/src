from otp.avatar.Avatar import Avatar
from otp.movie.Movie import Movie
from toontown.nametag import NametagGlobals
from toontown.suit import Suit, SuitDNA
from toontown.toon import Toon, ToonDNA


class ToontownMovie(Movie):
    def __init__(self):
        Movie.__init__(self)

        self.toons = set()
        self.suits = set()

    def createToon(self, name='', dna=None, addActive=False):
        toon = Toon.Toon()

        toon.setName(name)
        toon.setPickable(0)
        toon.setPlayerType(NametagGlobals.CCNonPlayer)

        if addActive:
            toon.addActive()

        if not isinstance(dna, ToonDNA.ToonDNA):
            if isinstance(dna, basestring):
                dna = ToonDNA.ToonDNA(str=dna)
            else:
                dna = ToonDNA.ToonDNA()
                dna.newToonRandom(seed=dna)

        toon.setDNA(dna)

        toon.animFSM.request('neutral')
        toon.reparentTo(hidden)

        self.toons.add(toon)
        return toon

    def createSuit(self, name='', dna=None, addActive=False):
        suit = Suit.Suit()

        suit.setDisplayName(name)
        suit.setPickable(0)

        if addActive:
            suit.addActive()

        if not isinstance(dna, SuitDNA.SuitDNA):
            if isinstance(dna, basestring):
                dna = SuitDNA.SuitDNA(str=dna)
            else:
                dna = SuitDNA.SuitDNA()
                dna.newSuitRandom()

        suit.setDNA(dna)

        suit.loop('neutral')
        suit.reparentTo(hidden)

        self.suits.add(suit)
        return suit

    def cleanup(self):
        for toon in list(self.toons):
            if toon in Avatar.ActiveAvatars:
                toon.removeActive()
            toon.delete()
            self.toons.remove(toon)

        for suit in list(self.suits):
            if suit in Avatar.ActiveAvatars:
                suit.removeActive()
            suit.delete()
            self.suits.remove(suit)

        Movie.cleanup(self)
