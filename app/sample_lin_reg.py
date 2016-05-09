def step_gradient(s_current, b_current, m_current, r_current, points, learning_rate):
	s_gradient = 0
	b_gradient = 0
	m_gradient = 0
	r_gradient = 0
	OG_fit = 100
	fits = [1, .9, .93, .91]

	N = float(len(points))
	for i in range(0, len(points)):
		x = points[i][0]
		y = points[i][1]
		z = points[i][2]
		current_fit = fits[i]
		s_gradient += -(2/N) * (fits[i] - ((b_current * x) + (m_current * y) + (r_current * z) + (s_current)))
		b_gradient += -(2/N) * x * (fits[i] - ((b_current * x) + (m_current * y) + (r_current * z) + (s_current)))
		m_gradient += -(2/N) * y * (fits[i] - ((b_current * x) + (m_current * y) + (r_current * z) + (s_current)))
		r_gradient += -(2/N) * z * (fits[i] - ((b_current * x) + (m_current * y) + (r_current * z) + (s_current)))

	new_s = s_current - (learning_rate * s_gradient)
	new_b = b_current - (learning_rate * b_gradient)
	new_m = m_current - (learning_rate * m_gradient)
	new_r = r_current - (learning_rate * r_gradient)
	return [new_s, new_b, new_m, new_r]

def gradient_descent_runner(points, start_s, start_b, start_m, start_r, learning_rate, num_iters):
	s = start_s
	b = start_b
	m = start_m
	r = start_r

	for i in range(num_iters):
		s, b, m, r = step_gradient(s, b, m, r, points, learning_rate)

	print("S: ", s)
	print("B: ", b)
	print("M: ", m)
	print("R: ", r)
	expec_one = s + (b * points[0][0]) + (m * points[0][1]) + (r * points[0][2])
	expec_two = s + (b * points[1][0]) + (m * points[1][1]) + (r * points[1][2])
	expec_three = s + (b * points[2][0]) + (m * points[2][1]) + (r * points[3][2])

	print("Expect One: ", expec_one)
	print("True Fit: ", 1)
	print("Expect Two: ", expec_two)
	print("True Fit: ", .9)
	print("Expect Three: ", expec_three)
	print("True Fit: ", .93)
	return [s, b, m, r]
def run():
	points = [[.80, .9, .56], [.85, .8, .50], [.76, .77, .59], [.81, 1, .423]]
	avg_points = [3.4, 380000, 34]
	learning_rate = .05

	initial_s = 0#y intercept (?)
	initial_b = 0
	initial_m = 0
	initial_r = 0

	num_iters = 1000

	[s, b, m, r] = gradient_descent_runner(points, initial_s, initial_b, initial_m, initial_r, learning_rate, num_iters)

	print

if __name__ == '__main__':
	run()



