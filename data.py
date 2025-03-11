import numpy as np

# Initialize data
inverter_flags = [('DCOV', 1), ('DCUV', 1), ('DRV', 1), ('ACOC', 1), ('CTRT', 1), ('MTRT', 1), ('SWF', 0), ('SGF', 0), ('CANF', 0)]
battery_flags = [('BOV', 1), ('BUV', 0), ('B T', 1), ('D OC', 0), ('C OC', 0), ('COM', 1), ('LEAK', 1)]
IMD_flags = [('GNDF', 0), ('ERR', 1), ('UV', 1), ('INSF', 0)]
battery_pack = {'voltage': 0, 'current': 0, 'temp': 0, 'soc': 0}
cell_volts = np.random.uniform(low=3.2, high=4.2, size=(16, 7))
cell_temp = np.random.uniform(low=20, high=45, size=(16, 7))
dti_temp = {'motor': 0, 'inverter': 0}
speed = 50
pps_counter = 0