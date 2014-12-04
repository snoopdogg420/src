from direct.distributed.DistributedObject import DistributedObject


class DistributedScienceFair(DistributedObject):
    def generate(self):
        DistributedObject.generate(self)
        # Load models here

    def delete(self):
        DistributedObject.delete(self)
        # Remove models here
