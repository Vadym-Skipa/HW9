from time import sleep

class VacuumCleanerError(Exception):
    pass

class IncorrectBatteryCharge(VacuumCleanerError):
    pass

class IncorrectAmountOfWater(VacuumCleanerError):
    pass

class IncorrectGarbageBinOccupancy(VacuumCleanerError):
    pass

class LowBatteryCharge(Exception):
    pass

class VacuumCleaner:

    config = {"waste_difference": 17, "water_difference": 0.3, "battery_difference": 2}
    actions_with_low_battery = 5

    def __init__(self, battery_charge, amount_of_water, garbage_bin_occupancy):
        try:
            self.battery_charge = battery_charge
            self.amount_of_water = amount_of_water
            self.garbage_bin_occupancy = garbage_bin_occupancy
        except VacuumCleanerError as error:
            print("Incorrect input params")
            raise error
        except LowBatteryCharge:
            pass
        try:
            with open("vacuum_cleaner.conf") as config:
                for line in config:
                    key = line.split()[0]
                    value = float(line.split()[-1])
                    self.config[key] = value
        except FileNotFoundError:
            print("Config is not found, using default values")

    @property
    def battery_charge(self):
        return self._battery_charge

    @battery_charge.setter
    def battery_charge(self, battery_charge):
        if 15 < battery_charge <= 100:
            self._battery_charge = battery_charge
        elif 0 < battery_charge <= 15:
            self._battery_charge = battery_charge
            raise LowBatteryCharge
        else:
            raise IncorrectBatteryCharge

    @property
    def amount_of_water(self):
        return self._amount_of_water

    @amount_of_water.setter
    def amount_of_water(self, amount_of_water):
        if amount_of_water >= 0:
            self._amount_of_water = amount_of_water
            self._washing_enable = True
        else:
            raise IncorrectAmountOfWater

    @property
    def garbage_bin_occupancy(self):
        return self._garbage_bin_occupancy

    @garbage_bin_occupancy.setter
    def garbage_bin_occupancy(self, garbage_bin_occupancy):
        if 0 <= garbage_bin_occupancy <= 100:
            self._garbage_bin_occupancy = garbage_bin_occupancy
            self._cleaning_enable = True
        else:
            raise IncorrectGarbageBinOccupancy

    def wash(self):
        if self._washing_enable and self.battery_charge != 0:
            try:
                self.amount_of_water -= self.config["water_difference"]
                try:
                    self.battery_charge -= self.config["battery_difference"]
                except LowBatteryCharge:
                    print("Low charge")
                    self.actions_with_low_battery -= 1
                print("Wash")
            except IncorrectAmountOfWater:
                print("The water is over.")
                self._washing_enable = False
        else:
            print("Don't washing")

    def vacuum_cleaner(self):
        if self._cleaning_enable and self.battery_charge != 0:
            try:
                self.garbage_bin_occupancy += self.config["waste_difference"]
                try:
                    self.battery_charge -= self.config["battery_difference"]
                except LowBatteryCharge:
                    print("Low charge")
                    self.actions_with_low_battery -= 1
                print("vacuum cleaner")
            except IncorrectGarbageBinOccupancy:
                print("The garbage bin is full.")
                self._cleaning_enable = False

    def move(self):
        self.actions_with_low_battery = 5
        while self.actions_with_low_battery > 0 and (self._cleaning_enable or self._washing_enable):
            print("Move ---")
            print(f"battery {self.battery_charge} water {self.amount_of_water} trash {self.garbage_bin_occupancy}")
            self.wash()
            self.vacuum_cleaner()
            sleep(1)

v = VacuumCleaner(90, 1, 20)
v.move()
