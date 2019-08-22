"""
Developed by Fraser Love
On 22/08/19
"""
from qiskit import QuantumCircuit, visualization, execute, IBMQ, Aer
import matplotlib.pyplot as pl

provider = IBMQ.load_account().get_backend('ibmqx4')
#provider = Aer.get_backend('qasm_simulator')

# Setting up the q-bit and classical-bit buffers
qc = QuantumCircuit(4, 2)
# Pauli X gate used to initialise qbits to 1, comment out to set inputs to 0
qc.x(0)
qc.x(1)
# Calculate the sum bit using C-NOT gates
qc.cx(0,2)
qc.cx(1,2)

# Calculate the carry bit using ccX (Toffoli) gate
qc.ccx(0,1,3)

# Measure the qbits and store in classical registers
qc.measure([2,3], [0,1])

# Executing quantum circuit and storing results
result = execute(qc, provider).result()
counts = result.get_counts(qc)
# Displaying results on screen and creating a histogram
print(counts)
plot = visualization.plot_histogram(counts)
plot.savefig('/Users/fraser/Desktop/test.png')
