from toontown.building.DistributedElevatorExtAI import DistributedElevatorExtAI


class DistributedCogdoElevatorExtAI(DistributedElevatorExtAI):
    notify = directNotify.newCategory('DistributedCogdoElevatorExtAI')

    def _createInterior(self):
        self.bldg.createCogdoInterior()
