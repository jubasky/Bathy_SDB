class Chair(object):
    """This class represents chairs."""
    def __init__(self, name, legs=4):
        self.name = name
        self.legs = legs


chair2 = Chair("Bar Stool", 1)

print(chair2.name)