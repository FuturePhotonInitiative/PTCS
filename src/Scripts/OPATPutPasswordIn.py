# the laser cannot be successfully turned on without it being unlocked
def main(data_map, results):
    laser = data_map["Devices"]["Laser Source"]

    print(laser.enter_password())
