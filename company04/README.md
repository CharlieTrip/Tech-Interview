# Company 04


**Task tl;dr:** read a paper, implement it, do some analysis and write a report.


## Company's Feedback

Positive feedback, they acknowledged the efforts and quality of the assessment.


## Opinion and Grade

I appreciated the feedback and the transparency of the whole hiring process.

The task was definitely well-designed and the suggested paper is self-contained, well written
and of high quality in general.
The task was challenging but not impossible, the amount of work was coherent with the (1-week)
expectations and I had great fun working on it, despite I was in the middle of travelling
and relocating!

More assessments should be like this one seems to have a clear solving structure, each point
was (basically) one day for me:
1. read the content and plan what to do
2. design the code and start writing the report (e.g. notations, protocols, easy stuff)
3. write the code
4. finish writing 
5. clean-up and send

Maybe, to make it a perfect assessment, I would have appreciated a clearer goal for the
prototype since I went for the simplest mathematical structure to make the prototype
work but not that secure.


**Grade**: `95/100`, perfect assignment!


---

## Structure

+ `report.pdf`: the compiled report
+ `report/`: the TeX source of the report
+ `code/`: the code (check the repo for instructions)

---

## Task description

Prepare: 
+ a report answering the questions
+ the list of tools you have used
+ code you may have developed

A Proof of Sequential Work (PoSW) enables showing that some computation was going on for `T`
time steps since some statement was received.
A lattice-based construction of PoSW is given in LM24[^LM24].

1. Present in a high-level way the construction given in LM24 [^LM24].
	Explain the intuition behind it.

2. Fully specify the resulting protocol and prototype it with your favourite
	programming language/tool (e.g., Python, Sage, C++, Rust, ...).

3. Analyse the efficiency of the implementation in terms of memory, communication
	and computation requirements.

4. How to turn the above protocol into a non-interactive proof system?
	Write down the resulting system by fully specifying the different steps.

5. Present one or two applications of the previous protocol and/or system.


[^LM24]: Russell W. F. Lai and Giulio Malavolta.
	Lattice-Based Timed Cryptography. Cryptology ePrint Archive, Report 2024/540, 2024.
	Available on [eprint](https://eprint.iacr.org/2024/540);
	earlier version published in [Crypto 2023](https://doi.org/10.1007/978-3-031-38554-4_25)

