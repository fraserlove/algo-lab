from autodiff import MLP

# Example data
xs = [
    [2.0, 3.0, -1.0],
    [3.0, -1.0, 0.5],
    [0.5, 1.0, 1.0],
    [1.0, 1.0, -1.0]
]
ys = [1.0, -1.0, -1.0, 1.0] # Labels

x = [2.0, 3.0, -1.0]
n = MLP(2, [4, 4, 1])
print(len(n.parameters()))
n(x).graph().render('train', format='pdf', view=True, cleanup=True)

def loss(ys, ypreds):
    """Mean squared error loss."""
    return 0.5 * sum([(y - ypred)**2 for y, ypred in zip(ys, ypreds)])

max_iters = 200
lr = 0.002 # Learning rate

# Training loop. Gradient descent
for i in range(max_iters):
    # Forward pass
    ypreds = [n(x) for x in xs]
    l = loss(ys, ypreds)

    # Backward pass
    n.zero_grad()
    l.backward()

    # Update weights
    for param in n.parameters():
        param.v -= lr * param.dv

    if i % (max_iters // 10) == 0 or i == max_iters - 1:
        print(f'Iteration {i:2d} | Loss: {l.v:.4f}')

# Predictions
print('Predictions:', ypreds)