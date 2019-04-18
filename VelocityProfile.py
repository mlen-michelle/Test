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

def main():
	if len(sys.argv) < 2:
		sys.exit('Please pass a file name as first argument')
	else:
		graph_data = velocity_data(sys.argv[1])

	with open('R-Squared Value', 'w') as f:
		f.write('Timestep\tR-Squared\tSlope\n')
		sorted_graph_data = sorted(graph_data, key=lambda x: x['time'])

		for data in sorted_graph_data:
			a = data['time']
			b = data['r2']
			c = data['shear']
			f.write(str(a) + '\t' + str(b) + '\t' + str(c) + '\n')

if __name__ == '__main__':
	main()
