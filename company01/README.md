# Company 01

**tl;dr:** two prototyping problems, choose one. Provide a report and the code.


## Company's Feedback

No feedback.


## Opinion and Grade

I believe that their expectation was very high on the implementation which was not what I
considered important, especially after noticing that there is an attack and the paper points to
a protocol that doesn't exist.

The tasks are nice, not too challenging but open enough to explore how I work.
I initially started with one problem and then checked the other and ended up doing both,
especially after digesting the paper from Task A.
I believe that I was supposed to have an oral interview too where I would *"defend"/explain* my
report and code but this never happened.


**Grade**: `70/100`, the task was clear but expectations were not.
	We definitely don't have the same definition of *"prototype"*, I suppose.


---

## Structure

+ `report.pdf`: the compiled report
+ `report/`: the TeX source of the report
+ `code/`: the code (check the repo for instructions)

---


## Task description

Please choose one of the following 2 questions.

### Task A: Multi-Party Exponentiation
A company is developing a secure exponentiation protocol using multi-party computation.
Researchers are looking into the literature and have found Protocols 5 and 6 in
[this paper](https://eprint.iacr.org/2019/334.pdf).

1. Prove that these two protocols are secure (in say the UC framework) in the setting
	of malicious adversaries, or find suitable adversarial attacks. We would like to see how
	you think about and approach the problem, so a description of your approach would be helpful.
2. Whether it is secure or not, a small prototype would be helpful to the engineers.
	Please write a prototype for the protocols using the code below.
	Feel free to change the provided code.

**Bonus:** How can this be improved?
	Can you extend the code below to use shares?
	If it helps, there is code for Shamir secret sharing on Wikipedia.

```
from random import randrange

class Share:
	# Secret value
	_value: int

	def __init__(self, value):
		self._value = value
	def __repr__(self):
		return f"Share({self._value})"
        
class FiniteGroup:
# Modulus, i.e. p in Z/pZ group: int
	def __init__(self, group):
		self.group = group
	def add(self, left, right):
		value = (left._value + right._value) % self.group
		return Share(value)
	def sub(self, left, right):
		value = (left._value - right._value) % self.group
		return Share(value)
	def product(self, left, right):
		value = (left._value * right._value) % self.group
		return Share(value)
	def product_with_public(self, share, public):
		value = (share._value * public) % self.group
		return Share(value)
	def exp(self, base, exponent):
		if type(base) == int and type(exponent) == Share:
		power = pow(base, exponent._value, self.group)
		elif type(exponent) == int and type(base) == Share:
		power = pow(base._value, exponent, self.group)
		return Share(power)
	def public_exp(self, base, exponent):
		power = pow(base, exponent, self.group)
		return power
	def open(self, share):
		return share._value % self.group
	def share(self, value):
		return Share(value % self.group)
	def srand(self):
		# random value in multiplicative group
		return Share(randrange(1, self.group))
	def __repr__(self):
		return f"Z/{self.group}Z"
```


### Task B: Zero Knowledge Proof
A company is developing a new authentication protocol.

The company cryptographers have been investigating alternatives to password hashing and have
found that Zero-Knowledge Proof (ZKP) is a viable alternative to hashing in an authentication schema.
Moreover, the cryptographers have found Chaum–Pedersen Protocol to be suitable for this purpose.
See ["Cryptography: An Introduction (3rd Edition)"](https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf), page 377, section "3. Sigma Protocols", subsection "3.2. Chaum–Pedersen Protocol.

We want to adapt this protocol to support 1-factor authentication, that is, the exact matching of
a number (registration password) stored during registration and another number (login password)
generated during the login process.

As part of an agile team, you have accepted the challenge of prototyping the ZKP Protocol and a 
Proof-of-Concept application that utilizes the protocol to register and authenticate users.

Design and write the code that implements the ZKP Protocol.
The solution should implement two flavours: one with exponentiations (as described in the book) and
one using Elliptic Curve cryptography.

We would like to see how you are thinking about and approaching the problem, so a simple description
of your approach and how you’d extend it or integrate would be helpful.