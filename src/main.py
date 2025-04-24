import pandas as pd
import numpy as np
from algorithms.mowwo import MOWWO
from problems.medical_supply_scheduling import MedicalSupplyScheduling
from visualization import plot_pareto_front

def load_problem_from_csv(csv_path):
    # Example: Load your CSV and parse into the required dictionary for from_dict
    df = pd.read_csv(csv_path)
    # You must adapt this parsing to your actual CSV structure!
    # Here is a placeholder for demonstration:
    for idx, row in df.iterrows():
        data = {
        'm': int(df['m'][0]),
        'n': int(df['n'][0]),
        'K': int(df['K'][0]),
        'K1': int(df['K1'][0]),
        'K2': int(df['K2'][0]),
        'wk': eval(df['wk'][0]),
        'ro': eval(df['ro'][0]),
        'rs': eval(df['rs'][0]),
        'rm': eval(df['rm'][0]),
        'rv': eval(df['rv'][0]),
        'aik': np.array(eval(df['aik'][0])),
        'ajk': np.array(eval(df['ajk'][0])),
        'cijk': np.array(eval(df['cijk'][0])),
        'cjjk': np.array(eval(df['cjjk'][0])),
        'coij': np.array(eval(df['coij'][0])),
        'csij': np.array(eval(df['csij'][0])),
        'cmij': np.array(eval(df['cmij'][0])),
        'cvij': np.array(eval(df['cvij'][0])),
        'bjk': np.array(eval(df['bjk'][0])),
        'no_i': eval(df['no_i'][0]),
        'ns_i': eval(df['ns_i'][0]),
        'nm_i': eval(df['nm_i'][0]),
        'nv_i': eval(df['nv_i'][0]),
        'no_j': eval(df['no_j'][0]),
        'ns_j': eval(df['ns_j'][0]),
        'nm_j': eval(df['nm_j'][0]),
        'nv_j': eval(df['nv_j'][0]),
        'C': float(df['C'][0]),
        'S': float(df['S'][0])
    }
    
    return data

def main():
    # Load the sample data from CSV
    data = load_problem_from_csv('src/data/sample_instance.csv')
    
    # Initialize the medical supply scheduling problem
    problem = MedicalSupplyScheduling.from_dict(data)
    
    # Define objectives and constraints (replace with your actual functions)
    objectives = [problem.supply_satisfaction_rate, problem.scheduling_cost]
    constraints = []  # Add your constraint functions here

    # Set algorithm parameters
    population_size = 10
    max_iterations = 100

    # Initialize the MOWWO algorithm with all required arguments
    mowwo = MOWWO(population_size, max_iterations, objectives, problem, constraints)
    
    # Run the MOWWO algorithm
    results = mowwo.run()
    
    # Output the results
    print("Optimal Solutions:")
    for solution in results:
        print(solution)
        
    obj1_list = []
    obj2_list = []
    for sol in results:
        obj1, obj2 = problem.evaluate(sol['xijk'], sol['xjjk'], sol['yo'], sol['ys'], sol['ym'], sol['yv'])
        obj1_list.append(obj1)
        obj2_list.append(obj2)

    # When preparing data for plotting
    obj1_list = [satisfaction * 100 for satisfaction in obj1_list]  # Convert to percent

    # And update the label:
    plot_pareto_front(obj1_list, obj2_list, xlabel="Supply Satisfaction Rate (%)")

def run_optimization(instance_idx=0):
    import pandas as pd
    import numpy as np
    from problems.medical_supply_scheduling import MedicalSupplyScheduling
    from algorithms.mowwo import MOWWO

    df = pd.read_csv('src/data/sample_instance.csv')
    row = df.iloc[instance_idx]
    data = {
        'm': int(row['m']),
        'n': int(row['n']),
        'K': int(row['K']),
        'K1': int(row['K1']),
        'K2': int(row['K2']),
        'wk': eval(row['wk']),
        'ro': eval(row['ro']),
        'rs': eval(row['rs']),
        'rm': eval(row['rm']),
        'rv': eval(row['rv']),
        'aik': np.array(eval(row['aik'])),
        'ajk': np.array(eval(row['ajk'])),
        'cijk': np.array(eval(row['cijk'])),
        'cjjk': np.array(eval(row['cjjk'])),
        'coij': np.array(eval(row['coij'])),
        'csij': np.array(eval(row['csij'])),
        'cmij': np.array(eval(row['cmij'])),
        'cvij': np.array(eval(row['cvij'])),
        'bjk': np.array(eval(row['bjk'])),
        'no_i': eval(row['no_i']),
        'ns_i': eval(row['ns_i']),
        'nm_i': eval(row['nm_i']),
        'nv_i': eval(row['nv_i']),
        'no_j': eval(row['no_j']),
        'ns_j': eval(row['ns_j']),
        'nm_j': eval(row['nm_j']),
        'nv_j': eval(row['nv_j']),
        'C': float(row['C']),
        'S': float(row['S'])
    }
    problem = MedicalSupplyScheduling.from_dict(data)
    objectives = [problem.supply_satisfaction_rate, problem.scheduling_cost]
    constraints = []  # Add constraint functions if needed
    population_size = 10
    max_iterations = 100
    mowwo = MOWWO(population_size, max_iterations, objectives, problem, constraints)
    results = mowwo.run()
    obj1_list, obj2_list = [], []
    for sol in results:
        obj1, obj2 = problem.evaluate(sol['xijk'], sol['xjjk'], sol['yo'], sol['ys'], sol['ym'], sol['yv'])
        obj1_list.append(obj1 * 100)  # percent
        obj2_list.append(obj2)
    return obj1_list, obj2_list, results
if __name__ == "__main__":
    main()