"""
Developed by Fraser Love
On 25/08/19

A program using quantum gates to add two qbits together. Firstly a truth table is printed to
show the quantum full adder working properly and then it adds two superpositions together.
"""

from qiskit import QuantumCircuit, visualization, execute, IBMQ
import matplotlib.pyplot as pl

plot_results = True

provider = IBMQ.load_account().get_backend('ibmq_qasm_simulator')

truth_table = ([a, b, cin] for a in range(0,2) for b in range(0,2) for cin in range(0,2))

def init_qbits(qc, row):
    print('{}\t{}\t{}\t'.format(row[0], row[1], row[2]), end='')
    if row[0] == 1:
        qc.x(0)
    if row[1] == 1:
        qc.x(1)
    if row[2] == 1:
        qc.x(2)

def full_adder(qc):
    # Calculates the sum and carry out using Toffoli and CNOT gates
    qc.ccx(0,1,3)
    qc.cx(0,1)
    qc.ccx(1,2,3)
    qc.cx(1,2)
    qc.cx(0,1)
    
    # Measuring the value of the qbits
    qc.measure([2,3], [0,1])

def calc_truth_table():
    # Creates a truth table to show the full adder working
    print('----------------Truth Table----------------')
    print('A\tB\tCin\tSum\tCout')
    
    for row in truth_table:
        qc = QuantumCircuit(4, 2)
        init_qbits(qc, row)
        
        full_adder(qc)
        
        result = execute(qc, provider).result()
        print('{}\t{}'.format(list(result.get_counts(qc).keys())[0][1], list(result.get_counts(qc).keys())[0][0]))
    
    print('-------------------------------------------')

def superpos():
    # Qbit 2 is initialised to 0 and qbits 0 and 1 are initialised to a superposition using the Hadamard gate
    qc = QuantumCircuit(4, 2)
    qc.h(0)
    qc.h(1)
    
    full_adder(qc)
    
    result = execute(qc, provider).result()
    counts = result.get_counts(qc)
    print("Superposition Results:", counts)
    if plot_results:
        plot = visualization.plot_histogram(counts)
        plot.savefig('superpos.png')

def run():
    calc_truth_table()
    superpos()

run()
