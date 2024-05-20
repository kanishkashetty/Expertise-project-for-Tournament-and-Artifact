
#This simulation code calculate the solver utility and its impact on the tournament cost, and visually represents how budget allocation influences both metrics.
#And satisfy model assumption that higher solver utility in the artifact leads to reduced effort costs in the tournament projects.

# Librarie
import numpy as np
import sympy as sym
import scipy.integrate as spi
import matplotlib.pyplot as plt

# Model Parameters
n_a = 2
theta_a = 0.5
c_a = 0.1
cBase_t = 5.0
cVar_t = 2.0
solvUtilMax_a = 100

# Define distribution functions for expertise in artifact
def f_a(beta):
    z = (beta - 100)/10
    return 1/10.0 * np.exp(-z + np.exp(-z))

def F_a(beta):
    z = (beta - 100)/10
    return np.exp(-np.exp(-z))

# Calculate solver utility for a given amount allocated to artifact
def seekerUtilityamountA_a(rho, n, beta_l_a, beta_u_a, theta, A, c, F, f):
    def eq1(beta):
        return theta * np.log(A) * n * F(beta)**(n-1) * f(beta)

    def eq2(beta):
        return theta * np.log(A) * f(beta)

    term1, _ = spi.quad(eq1, beta_l_a, beta_u_a)
    term2, _ = spi.quad(eq2, beta_l_a, beta_u_a)
    return rho * term1 + (1 - rho) * term2

# Compute solver utility and cost of effort for different budget allocations
A_a_values = range(1, 101)
solverUtility_a_values = []
c_t_values = []

for A_a in A_a_values:
    solverUtility_a = seekerUtilityamountA_a(rho=1, n=n_a, beta_l_a=75, beta_u_a=375, theta=theta_a, A=A_a, c=c_a, F=F_a, f=f_a)
    solverUtility_a_values.append(solverUtility_a)
    c_t = cBase_t + (solverUtility_a / solvUtilMax_a) * (cVar_t - cBase_t)
    c_t_values.append(c_t)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(A_a_values, solverUtility_a_values, label='Solver Utility')
plt.plot(A_a_values, c_t_values, label='Cost of Effort (c_t)', color='red')
plt.xlabel('Budget Allocated to Artifact (A_a)')
plt.ylabel('Value')
plt.title('Solver Utility and Cost of Effort - Budget Allocation to Artifact')
plt.legend()
plt.grid(True)
plt.show()
