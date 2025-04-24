import matplotlib.pyplot as plt

def plot_pareto_front(objective1, objective2, title="Pareto Front", xlabel="Supply Satisfaction Rate", ylabel="Cost Objective"):
    plt.figure(figsize=(8,6))
    plt.scatter(objective1, objective2, c='blue', label='Pareto Solutions')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()