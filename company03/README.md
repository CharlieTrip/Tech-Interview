# Company 03


**Task tl;dr:** read some papers and reply to some questions.


## Company's Feedback

A filtered couple of sentences from a longer unshared feedback:
there are some imprecisions in the report and there is a mixing of two parameters which leads to 
an incorrect analysis for achieving 128 bits of security.

No more than this.



## Opinion and Grade

The task was hard for me and my background.
The questions are extremely specific and I had to bootstrap quite a lot of background
to even approach the task.

It is fair considering the job was 100% on this topic meaning I was not a good fit.
To find all the necessary information, I had to carefully dig into the details of 10 different
papers and I am still unsure of how the parameters interweave.

From my point of view, the task is not good.

Both papers are (IMHO) poorly written because, even after getting some background on the topic,
the answers seem to not be *in* the papers.
Ok, fair.
A lot of published papers provide deliberately obfuscated results.

On the other hand, the feedback is horrible.
*How can I assess whether I was wrong or not?*

Since the task is (basically) a university exam, I would have appreciated receiving the
*"solutions"* to understand *why* I'm wrong, especially because of the readability of the papers.


**Grade**: `20/100`, bad papers, horrible feedback.


---

## Structure

+ `report.pdf`: the compiled report
+ `report/`: the TeX source of the report

---

## Task description

FRI-based polynomial commitment schemes are commonly used for building transparent zkSNARKs.

Some variants of such schemes have a wide range of parameters for finding a trade-off between
the performance and security of the overall system.
For example, a larger proximity parameter of the FRI protocol allows for a more efficient commitment
scheme but requires careful consideration when analyzing the system's security level.

We propose to consider two specific proof systems, Redshift[^redshift] and Plonky2[^plonky2]
	(both use the FRI-based commitment scheme), and answer the following research questions.

1. Redshift describes ways to guarantee the uniqueness of setup polynomials (see section 4.3 [^redshift]).
	Namely, they propose to use extra evaluation points. How many extra points will ensure a 128-bit
	security level for a 256-bit finite field and code rate = 1/8?
2. Describe (briefly) how an attacker can exploit the absence of such extra points.
3. Does the Soundness notion capture such types of attacks?
4. Does Plonky2 use extra evaluation points? If yes, how many are used? Why exactly so many?
	If not, is the system still safe to use? Why?
5. Can the attack described in the first answer be applied to Plonky2?

To prepare your answers, you may need to refer to the source code of these proof systems.
We expect you to prepare your answer using LaTeX.

[^redshift]: Kattis, A., Panarin, K., & Vlasov, A. (2019).
	RedShift: Transparent SNARKs from List Polynomial Commitment IOPs. IACR Cryptol. ePrint Arch., 2019, 1400.

[^plonky2]: Polygon Zero Team (2022).
	Plonky2: Fast Recursive Arguments with PLONK and FRI.
	[Link](https://github.com/0xPolygonZero/plonky2/blob/main/plonky2/plonky2.pdf)