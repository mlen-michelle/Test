from scipy import stats
from VelocityProfileParser import VelocityProfileParser
import sys

def velocity_data(filename):
    all_data = VelocityProfileParser(filename).all_steps
    all_velocity_details = {}

    graph_data = []
    for timestep in all_data:
        timestep_details = all_data[timestep]
        all_velocity_details[timestep] = []
        coord = []
        speed = []
        for data in timestep_details:
            coord.append(float(data[1]))
            speed.append(float(data[3]))
            step_details = [coord, speed]
            all_velocity_details[timestep] = step_details
        # slope, intercept, r_value, p_value, std_err = stats.linregress(coord[1:9], speed[1:9])
        slope, intercept, r_value, p_value, std_err = stats.linregress(coord[1:-1], speed[1:-1])

        graph_datum = {
            'time': timestep,
            'r2': r_value**2,
            'shear': slope
        }

        graph_data.append(graph_datum)

    return graph_data

if len(sys.argv) < 2:
    sys.exit('please pass a filename as first argument')
graph_data = velocity_data(sys.argv[1])

new_file = open('R-Squared Value', 'w')
new_file.write('Timestep \t R-Squared \t Slope \n')
sorted_graph_data = sorted(graph_data, key=lambda x: x['time'])

for data in sorted_graph_data:
    a = data['time']
    b = data['r2']
    c = data['shear']
    new_file.write(str(a) + '\t' + str(b) + '\t' + str(c) + '\n')

new_file.close()

