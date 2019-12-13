
# it takes a good amount of seconds after turning the laser on for the opm do get acclimated to
# reading a different range of light
def main(data_map, results):
    """
    obtain data from the optical power meter based on what power the laser is outputting
    """
    laser = data_map["Devices"]["Laser Source"]
    opm = data_map["Devices"]["Newport OPM"]

    opm_wavelength = data_map["Data"]["Initial"]["opm_wavelength"]
    laser_wavelength = data_map["Data"]["Initial"]["laser_wavelength"]
    laser_power1 = data_map["Data"]["Initial"]["laser_power1"]
    laser_power2 = data_map["Data"]["Initial"]["laser_power2"]
    reading_units = data_map["Data"]["Initial"]["reading_units"]

    data_map["Data"]["Collect"] = {}
    data_map["Data"]["Collect"][str(laser_power1)] = []
    data_map["Data"]["Collect"][str(laser_power2)] = []

    opm.make_outputs_unverbose()
    opm.turn_off_attenuator()
    opm.set_wavelength(opm_wavelength)
    opm.change_reading_units(reading_units)

    laser.set_wavelength(laser_wavelength)
    orij = str(laser.get_optical_power())
    laser.set_optical_power(laser_power1)
    print(("switching power of the laser from " + orij + " to " + str(laser.get_optical_power())))

    laser.turn_laser_on()
    print("running first part")

    for i in range(70):
        data_map["Data"]["Collect"][str(laser_power1)].append(opm.get_power_reading())

    laser.turn_laser_off()
    orij = str(laser.get_optical_power())
    laser.set_optical_power(laser_power2)
    print(("switching power of the laser from " + orij + " to " + str(laser.get_optical_power())))
    laser.turn_laser_on()
    print("running second part")

    for i in range(70):
        data_map["Data"]["Collect"][str(laser_power2)].append(opm.get_power_reading())

    laser.turn_laser_off()
