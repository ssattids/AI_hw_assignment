
def get_transition_function(size, file):
    transition_f = []
    for i in range(size):
        line = file.readline()[0:-1] #remove /n character
        string_arr = (line.split(","))
        floats_arr = list(map(float, string_arr))
        transition_f.append(floats_arr)
        
    return transition_f

#preprocess the file to get all the data from the MDP file
def get_all_MDP_data (file_name):
    fh = open(file_name, "r")

    size = int(fh.readline())
    
    reward_for_states = []
    for i in range(size):
        state_reward = float(fh.readline())
        reward_for_states.append(state_reward)
    
    Left = get_transition_function(size, fh)
    Up = get_transition_function(size, fh)
    Right = get_transition_function(size, fh)
    Down = get_transition_function(size, fh)

        
    fh.close()
    
    return [size, reward_for_states, Left, Up, Right, Down]


def max_action_over_sum(index, all_actions, U):
    all_action_expectation = []
    for action in all_actions:
        P_s_prime_given_s_a = action[index]
        #element wise multiplication
        action_expectation = sum([P_s_prime_given_s_a[j] * U[j] for j in range(len(U))])
        all_action_expectation.append(action_expectation)
    max_action_util = max(all_action_expectation)
    return [max_action_util, all_action_expectation.index(max_action_util)]

def run_value_iteration (file_name):
    print("Results for " + file_name)
    size, rewards, Left, Up, Right, Down = get_all_MDP_data (file_name)
    
    all_actions = [Left, Up, Right, Down]
    
    #initialize Utility array 
    U1 = [0] * size
    s_action = [0] * size
    gamma = 1
    epsilon = 0.001
    
    #Value iteration algorithm
    k = 0
    while(True):
        U = U1[:]
        delta = 0
        
        for i in range(size):
            max_action_util, max_action = max_action_over_sum(i, all_actions, U)
            U1[i] = rewards[i] + gamma * max_action_util
            s_action[i] = max_action
            delta = max(delta, abs(U1[i] - U[i]))
    
        if (delta < epsilon):
            break
        
        k = k + 1
        if (k > 10000):
            print("Taking too long - broke early!")
            break
        
    print("State utilities")
    print(U1)
    
    direction_action = []
    #last state is abosrbing state so we dont care about that
    for i in s_action[0:-1]:
        if (i==0):
            direction_action.append("Left")
        if (i==1):
            direction_action.append("Up")
        if (i==2):
            direction_action.append("Right")
        if (i==3):
            direction_action.append("Down")
    print("Optimal policies")        
    print(direction_action)
    
    
run_value_iteration("GW1.txt")
print("\n")
run_value_iteration("GW2.txt")
        
