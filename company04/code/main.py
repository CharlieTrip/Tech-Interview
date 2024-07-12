from posw import PoSW
import time
from tqdm import tqdm
import numpy as np
import argparse


# Utility Function

def printstats(numbers,name):
	"""
	Print minimal statistic values
	"""
	mean = np.mean(numbers)
	variance = np.var(numbers)
	std_dev = np.std(numbers)
	median = np.median(numbers)
	print(">> ", name)
	print(f"Mean: \t\t\t{mean}")
	print(f"Variance: \t{variance}")
	print(f"St. Dev: \t\t{std_dev}")
	print(f"Median: \t\t{median}")
	


"""
	PoSW prototype
	Main testing code with minimal timing measurements	
	
	+ Instantiate the PoSW
	+ Generate a challenge
	+ Emulates the communication between prover and verifier

"""

def tests(p, q, a, n, T, secpar, f, m, tests):
	
	# Generate S for the specific ring Z
	S = [a,a+1]
	
	posw = PoSW(secpar=secpar, p=p, q=q, f=f, S=S, n = n)
	
	results = []
	eval_times = []
	prove_times = []
	
	for _ in tqdm(range(tests), desc="Testing",
			bar_format="{desc}: {percentage:3.0f}% | {n_fmt}/{total_fmt} ({remaining})",leave=False):
		A,x = posw.generate()
		
		ste = time.time()
		y,w = posw.evaluate(A,x,T)
		ete = time.time()
		te = (ete - ste) * 1000
		
		# Initialise the prover and verifier internal status
		
		Sp = [A,x,y,p,T,w]
		Sv = [A,x,y,p,T,None]
		res = None
		
		stp = time.time()
		while res == None:
			# Executes Prover step (output u)
			u, Sp = posw.prove(Sp[0],Sp[1],Sp[2],Sp[3],Sp[4],Sp[5],Sv[5])
			# Executes Verifier step (output r if necessary as Sv[5])
			res, Sv = posw.verify(u,Sv[0],Sv[1],Sv[2],Sv[3],Sv[4],Sv[5])
		etp = time.time()
		
		tp = (etp - stp) * 1000
		
		results.append(res)
		eval_times.append(te)
		prove_times.append(tp)
	
	print("Passing Rate:", results.count(True)/tests)
	print()
	printstats(eval_times,"Evaluation Time (ms)")
	print()
	printstats(prove_times,"Proving Time (ms)")
	

"""
	System Parameters
	
	+ p : base of the p-ary representation
	+ q : modulus of R_q
	+ a : used to create the subtractive list
	+ n : dimension of the PoSW
	+ T : sequential computations
	
	Parameters not used in the current prototype
	+ secpar : security parameter
	+ f : f-th root of unity (order)
	+ m : dimension of the PoSW
	
	Tests parameters
	+ tests : number of tests
"""

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="PoSW Prototype using ZZ")
	parser.add_argument('--p', type=int, default=19, help="Base of the p-ary representation")
	parser.add_argument('--q', type=int, default=101, help="Modulus of R_q")
	parser.add_argument('--a', type=int, default=0, help="Used to create the subtractive list")
	parser.add_argument('--n', type=int, default=10, help="Dimension of the PoSW")
	parser.add_argument('--T', type=int, default=100, help="Amount of sequential computations")
	parser.add_argument('--secpar', type=int, default=1, help="Security parameter (not used)")
	parser.add_argument('--f', type=int, default=1, help="f-th root of unity (not used)")
	parser.add_argument('--m', type=int, default=1, help="Dimension of the PoSW (not used)")
	parser.add_argument('--tests', type=int, default=100, help="Description for tests")
	args = parser.parse_args()
	tests(args.p, args.q, args.a, args.n, args.T, args.secpar, args.f, args.m, args.tests)
