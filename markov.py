# Markov Chaing Analysis

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 


o_data = pd.read_csv("data.csv", sep=",", header = 0)
#print(o_data.head())
lat_col = "avg_latency"
print("\n---------- TRY USING MARKOV CHAIN --------------")

# 1) define N possible states
# Possible states : low_latency (latency < 1000ms)
#					high_latency (latency > 1000ms)
# But we define that the outcome of a state is not fixed,
# but rather a probabilistic function of each state
#    - this is, one state can produce a number of outcomes based on a unique pdf
#    - so, the state sequence is not observable, but can be approximated from
#      the sequence of observations produced by the system
# In this sense, possible states become
#				state:  1) poor_connection, with observations: low_latency, high latency
#                       2) good_connection, with observations:  low_latency, high latency
# 2) At regular times the system transitions
# 3) Define state transition probability


# Get observation probabilities  b(k) = p{o = v_k| qi = s_k}

# use mean to set a threshold for low and high latency
thresh = o_data[lat_col].mean()
std_dev = o_data[lat_col].std()
#print (thresh,std_dev)

# get number of data points
n = len(o_data[lat_col])*1.0
# probabilities are simply:  data_points_of_xtype / total number of data points
# pl = probability low latency 
# ph = probability high latency
# pa = probability of average latency
pl = len( o_data[ o_data[lat_col] <= (thresh-std_dev) ]  )/n
ph = len( o_data[ o_data[lat_col] >= (thresh+std_dev) ] )/n
temp = o_data[ ((thresh-std_dev) <= o_data[lat_col]) ] 
temp = temp[ (temp[lat_col] <= (thresh+std_dev))]
pa = len( temp[lat_col] )/n
# sum must be 1.0

print("Emission probs: pl: {:.4f}, pa: {:.4f}, ph: {:.4f}".format(pl,pa,ph))

# define initial states probability:poor connection state (pc_s)= 0.3, (gc_s) good connection state = 0.7
pc_s = 0.3
gc_s = 0.7



def label_latencies(data, labels, intervals):

	# make as many comparisons as intervals present
	#print (len(intervals)-1)
	for i in range(0,len(intervals)-1):
		#print("interval {}".format(i))
		# extract lower and higher bounds in each interval
		(low, high) = (intervals[i], np.roll(intervals, -1)[i])
		if ( (data >= low) and (data < high) ):
			return labels[i]

def forward_propagation(i_pdf, states, st_matrix, em, e_pdf, obs,  T, c):
	"""
	Forward propagation algorithm
	initial_pdf = initial prob distribution of states
	st_matrix = state transition st_matrix
	e_pdf = emission probability distribution
	obs = observations
	T = total number of time steps
	"""
	if (T == 0):
		# based on the state provided calculate its probability
		state_index = np.argwhere( states == c)[0]
		isp = i_pdf[state_index][0]

		# now given the first observation
		# find its probability given the initial state
		# but first find the index of this emission
		em_index =  np.argwhere(em == obs.at[T])[0]
		# with these index and the state, the probability can be retrieved
		iep = e_pdf[state_index][0][em_index][0]
		#print("["+str(T)+"] State : "+c+" {:.4f} ".format(isp)+" , Emi: "+str(obs.at[T])+" {:.4f}".format(iep))
		# calculate initial prob
		a_i = isp*iep
		return (a_i)
	else:
		# get cumulative prob
		sums = 0.0
		current_state_index = np.argwhere(states==c)[0]
		for s in states:
			a = forward_propagation(i_pdf, states, st_matrix, em, e_pdf, obs,  T-1, s)
			# retrieve transition probability
			prev_state_index = np.argwhere(states==s)[0]
			aij = st_matrix[prev_state_index][0][current_state_index][0]
			# calculate past probability
			sums = sums + a*aij
		# get index for emmision at time T	
		em_index =  np.argwhere(em == obs.at[T])[0]	
		# with these index and the state, the 
		# emision probability can be retrieved
		ep = e_pdf[current_state_index][0][em_index][0]
		# get emission prob for current sate
		a_t = sums * ep
		#print("["+str(T)+"] State : "+c+" {:.4f} ".format(sums)+" , Emi: "+str(obs.at[T])+" {:.4f}".format(ep))
		return (a_t)

def viterbi(i_pdf, states, st_matrix, em, e_pdf, obs,  T, c):
	"""
	Forward propagation algorithm
	initial_pdf = initial prob distribution of states
	st_matrix = state transition st_matrix
	e_pdf = emission probability distribution
	obs = observations
	T = total number of time steps
	"""
	global optimal_states

	if (T == 0):
		# based on the state provided calculate its probability
		state_index = np.argwhere( states == c)[0]
		isp = i_pdf[state_index][0]

		# now given the first observation
		# find its probability given the initial state
		# but first find the index of this emission
		em_index =  np.argwhere(em == obs.at[T])[0]
		# with these index and the state, the probability can be retrieved
		iep = e_pdf[state_index][0][em_index][0]
		#print("["+str(T)+"] State : "+c+" {:.4f} ".format(isp)+" , Emi: "+str(obs.at[T])+" {:.4f}".format(iep))
		# calculate initial prob
		delta_i = isp*iep
		return (delta_i)
	else:
		# get highest path probability
		best_path = 0.0
		optimal_state = "None"
		current_state_index = np.argwhere(states==c)[0]
		for s in states:
			a = viterbi(i_pdf, states, st_matrix, em, e_pdf, obs,  T-1, s)
			# retrieve transition probability
			prev_state_index = np.argwhere(states==s)[0]
			aij = st_matrix[prev_state_index][0][current_state_index][0]
			# calculate path probability

			path = a*aij
			if(path > best_path):
				best_path = path
				optimal_state = s


		
		#track the optimal state
		if(T == 1 ):
			# We do this because when calculating the optimal state for 
			# time 1, we can also append a None for state zero
			# right before appending the optimal state for time 1
			optimal_states.append("None")
			optimal_states.append(optimal_state)
		else:
			optimal_states.append(optimal_state)
		# get index for emmision at time T	
		em_index =  np.argwhere(em == obs.at[T])[0]	
		# with these index and the state, the 
		# emision probability can be retrieved
		ep = e_pdf[current_state_index][0][em_index][0]
		# get emission prob for current sate
		delta_t = best_path * ep
		#print("["+str(T)+"] Best Path : "+c+" {:.4f} ".format(best_path)+" , Emi: "+str(obs.at[T])+" {:.4f}".format(ep))
		return (delta_t)


# define state transition probability
#                    to
#                poor   good
# from    poor  0.3    0.7 
#         good  0.75   0.25
transition_pdf = np.array([ [0.3,0.7],[0.75,0.25] ])
# define initial condition
initial_pdf = np.array([pc_s,gc_s])
# define states
states = np.array(["poor","good"])
# define emission probability distribution
#              pl    pa    ph
#      poor c  0.6   0.3   0.1
#      good c  0.3   0.4   0.3
#  this is just for example to express that each staet
# will have its own emission probability distribution
# following both have the same
e_pd = np.array([[0.6,0.3,0.1],[0.3,0.4,0.3]])
# define emissions
e = np.array(["low","ave","high"])


# LABEL data
interv = np.array([min(o_data[lat_col])-1, thresh-std_dev, thresh+std_dev, max(o_data[lat_col])+1])
o_data['labels']=map(lambda x: label_latencies(x,e,interv),o_data[lat_col])


P_O_lambda = 0.0
time = 5 #len(o_data['labels'])
print(time)


print(" *****  FORWARD PROPAGATION ***** ")
for sk in states:
	seq_prob = forward_propagation(initial_pdf, states, transition_pdf, e, e_pd, o_data['labels'], time, sk)
	P_O_lambda = P_O_lambda + seq_prob

print ("P(O|lambda) : {}".format(P_O_lambda))


optimal = list()
optimal_states2 = list()

print(" *****  VITERBI ***** ")

optimal_path_prob = 0.0
for sk in states:
	optimal_states = list()
	path_prob = viterbi(initial_pdf, states, transition_pdf, e, e_pd, o_data['labels'], time, sk)
	if(path_prob > optimal_path_prob):
		optimal = optimal_states
		optimal_path_prob = path_prob

print(optimal)



#print (thresh)