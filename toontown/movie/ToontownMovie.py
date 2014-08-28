from otp.movie.Movie import Movie
from otp.nametag.NametagGroup import NametagGroup
from toontown.suit import Suit, SuitDNA
from toontown.toon import Toon, ToonDNA


class ToontownMovie(Movie):
    def __init__(self):
        Movie.__init__(self)

        self.toons = set()
        self.suits = set()

    def createToon(self, name='', dna=None):
        toon = Toon.Toon()

        toon.setName(name)
        toon.setPickable(0)
        toon.setPlayerType(NametagGroup.CCNonPlayer)

        if not isinstance(dna, ToonDNA.ToonDNA):
            dna = ToonDNA.ToonDNA()
            dna.newToonRandom(seed=dna)

        toon.setDNA(dna)

        toon.animFSM.request('neutral')
        toon.reparentTo(hidden)

        self.toons.add(toon)
        return toon

    def createSuit(self, name='', dna=None):
        suit = Suit.Suit()

        suit.setDisplayName(name)
        suit.setPickable(0)

        if dna is None:
            dna = SuitDNA.SuitDNA()
            dna.newSuitRandom()

        suit.setDNA(dna)

        suit.loop('neutral')
        suit.reparentTo(hidden)

        self.suits.add(suit)
        return suit

    def cleanup(self):
        Movie.cleanup(self)

        for toon in list(self.toons):
            toon.delete()
            self.toons.remove(toon)

        for suit in list(self.suits):
            suit.delete()
            self.suits.remove(suit)
