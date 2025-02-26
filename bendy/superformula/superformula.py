import numpy as np
import matplotlib.pyplot as plt

# computes the radius r for a given angle theta using the superformula
def superformula(theta, a, b, m, n1, n2, n3):
    term1 = np.abs((1 / a) * np.cos(m * theta / 4)) ** n2
    term2 = np.abs((1 / b) * np.sin(m * theta / 4)) ** n3
    r = (term1 + term2) ** (-1 / n1)
    return r

# generates a random normal superformula curve
def normal_superformula():
    m = np.random.randint(2, 10)  # symmetry / number of lobes
    n1 = np.random.uniform(0.5, 3)
    n2 = np.random.uniform(0.5, 3)
    n3 = np.random.uniform(0.5, 3)
    a, b = 1, 1  # keep proportions uniform
    
    theta = np.linspace(0, 2 * np.pi, 500)
    
    r = superformula(theta, a, b, m, n1, n2, n3)
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return (x, y)

def plot(x, y):
    plt.figure(figsize=(6,6))
    plt.plot(x, y, color=np.random.rand(3,))
    plt.axis("equal")
    plt.show()

plot(*normal_superformula())
