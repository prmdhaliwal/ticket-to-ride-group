"""Train card and train piece classes."""


class TrainCarCard:
    def __init__(self, colour):
        self.colour = colour

    def matches(self, route_colour):
        if self.colour == route_colour:
            return True

        if self.colour == "locomotive":
            return True

        return False


class TrainCar:
    def __init__(self, owner=None, route=None):
        self.owner = owner
        self.route = route
