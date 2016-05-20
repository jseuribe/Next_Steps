from numpy import loadtxt, zeros, ones, array, linspace, logspace

data = loadtxt('ex1data1.txt', delimiter=',')
print(data)

X = data[:, 0]
Y = data[:, 1]

print(X)
print(Y)

m = Y.size

it = ones(shape=(m,2))

it[:, 1] = X

theta = zeros(shape=(2,1))

iterations = 1500

alpha = 0.01

def compute_cost(X, Y, theta):
	m = Y.size

	predictions = X.dot(theta).flatten()

	sqErrors = (predictions - Y) ** 2

	J = (1.0 / (2 * m)) *sqErrors.sum()

	return J

def gradient_descent(X, Y, theta, alpha, num_iters):
	m = Y.size

	J_historY = zeros(shape=(num_iters, 1))

	for i in range(num_iters):
		predictions = X.dot(theta).flatten()

		errors_x1 = (predictions - Y) * X[:, 0]

		errors_x2 = (predictions - Y) * X[:, 1]

		theta[0][0] = theta[0][0] - alpha * (1.0 / m) * errors_x1.sum()
		theta[1][0] = theta[1][0] - alpha * (1.0 / m) * errors_x2.sum()

		J_historY[i, 0] = compute_cost(X, Y, theta)

	return theta, J_historY

a, b = gradient_descent(X, Y, theta, alpha, iterations)

print(a)
print(b)