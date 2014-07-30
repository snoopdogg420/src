from otp.movie.Movie import Movie
from otp.nametag.NametagGroup import *
from toontown.toon import Toon, ToonDNA
from toontown.suit import Suit, SuitDNA


class ToontownMovie(Movie):
    def __init__(self):
        Movie.__init__(self)

        self.toons = []
        self.suits = []

    def createToon(self, name='', dna=None):
        toon = Toon.Toon()

        toon.setName(name)
        toon.setPickable(0)
        toon.setPlayerType(NametagGroup.CCNonPlayer)

        if dna is None:
            dna = ToonDNA.ToonDNA()
            dna.newToonRandom()

        toon.setDNA(dna)

        toon.animFSM.request('neutral')
        toon.reparentTo(render)

        self.toons.append(toon)
        return toon

    def createSuit(self, name='', dna=None):
        suit = Suit.Suit()

        suit.setDisplayName(name)
        suit.setPickable(0)

        if dna is None:
            dna = SuitDNA.SuitDNA()
            dna.newSuitRandom()

        suit.setDNA(dna)

        suit.reparentTo(render)

        self.suits.append(suit)
        return suit

    def cleanup(self):
        Movie.cleanup(self)

        for toon in self.toons:
            toon.delete()

        for suit in self.suits:
            suit.delete()
