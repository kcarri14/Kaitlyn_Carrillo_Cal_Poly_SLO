import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean

#PART 3
transition_matrix = np.array([
    [0.86, 0.09, 0.01, 0.03, 0.01],  
    [0.01, 0.75, 0.07, 0.08, 0.09], 
    [0.01, 0.02, 0.74, 0.21, 0.02],  
    [0.21, 0.24, 0.22, 0.21, 0.12],  
    [0.01, 0.16, 0.05, 0.05, 0.73],  
])

#initialize the matrices
states_names = ["S1", "S2", "S3", "S4", "S5"]
number_states = len(states_names)
steps = 10
initial_prob = np.array([1/5] * number_states)

dp = np.zeros((steps + 1, number_states))
backpointer = np.zeros((steps + 1, number_states), dtype=int)
dp[0] = initial_prob

for s in range(1, steps + 1):
    for current in range(number_states):
        probs = dp[s - 1] * transition_matrix[:, current]
        dp[s][current] = np.sum(probs)
        backpointer[s][current] = np.argmax(probs)

#output
final_prob_S3 = dp[steps, 2]
print(f"probability of ending at state S3:{final_prob_S3}")
# print(dp)
# print(backpointer)

#traces back
path = [2]
for t in range(steps, 0, -1):
    path.append(backpointer[t, path[-1]])
path.reverse()
path_states = [states_names[i] for i in path]

print(" -> ".join(path_states))

#PART 4
# Emission matrix: E_prob from Part 4.1

#read data
timepoints_data = pd.read_csv("genemarkers_timepoints.tsv", sep='\t', index_col=0)
timepoints_values = timepoints_data.values
states_data = pd.read_csv("genemarkers_states.tsv", sep='\t', index_col=0)
states_value = states_data.values

#find length of data in order to make a matrix
num_timepoints = timepoints_values.shape[0]
num_states = states_value.shape[0]

E_scores = np.zeros((num_timepoints, num_states))

#for each cell find the euclidean distance

for t in range(num_timepoints):
    for s in range(num_states):
        dist = euclidean(timepoints_values[t], states_value[s])
        E_scores[t][s] = -dist**2

#Gaussian distribution        
sigma2 = 1e4   
E_scores_scaled = E_scores / sigma2
#normalize these scores
E_unnorm = np.exp(E_scores_scaled)
E_prob = E_unnorm / E_unnorm.sum(axis=1, keepdims=True)        

#print(E_scores)
#print(E_prob)

# count  = 0 
# for r in E_prob:
#     total = sum(r)
#     if total == 1:
#         count += 1
# print(count)        
#print("E_prob shape:", E_prob.shape)



# initialize Viterbi tables
V = np.zeros((num_timepoints, num_states))  # max probability of any path to state s at time t
#print("V shape:", V.shape)
B = np.zeros((num_timepoints, num_states), dtype=int)  # backpointers

# initialize from S0 to all states equally
V[0] = (1/5) * E_prob[0]
initial_prob = np.array([1/5] * number_states)

for t in range(1, num_timepoints):
    for current in range(num_states):
        probs = V[t-1] * transition_matrix[:, current] * E_prob[t][current]
        V[t][current] = np.max(probs)
        B[t][current] = np.argmax(probs)

#find the final state with highest probability
final_state = 2   
final_prob  = V[-1, final_state]

# print(V)
# print(B)

#trace back the most likely path
path = [final_state]
for t in range(num_timepoints - 1, 0, -1):
    path.append(B[t][path[-1]])
path.reverse()

path_names = [states_names[i] for i in path]
#output
print(f"Viterbi final probability : {final_prob:.6e}")
print(" -> ".join(path_names))




