class Bike():
    def __init__(self, gear, speed):
        self._gear = gear
        self._speed = speed

    def __str__(self):
        return 'Current Speed: {}\nCurrent Gear: {}\n'.format(self._speed, self._gear)

    def speedUp(self):
        self._speed += 1

    def applyBrake(self):
        self._speed -= 1

    def setGear(self, gear):
        self._gear = gear

    def stop(self):
        self._speed = 0

    def increaseGear(self):
        self._gear += 1

    def decrease(self, gear):
        self._gear = gear

class mountainBike(Bike):
    def __init__(self, gear, speed, suspension):
        Bike.__init__(self, gear, speed)
        self._suspension = suspension

    def setSuspension(self, suspension):
        self._suspension = suspension

class racingBike(Bike):
    def __init__(self, gear, speed, tyre):
        Bike.__init__(self, gear, speed)
        self._tyre = type

    def setType(self, tyre):
        self._tyre = tyre

class stuntBike(Bike):
    def __init__(self, gear, speed, seat_height):
        Bike.__init__(self, gear, speed)
        self._seat_height = seat_height

    def setHeight(self, height):
        self._seat_height = height
