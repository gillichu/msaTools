# msaTools

Merging Alignments
This code is adapted from the [SEPP](https://github.com/smirarab/sepp) codebase, so you'll need to have a working installation of SEPP. It also requires you to have installed the bundled HMMER executables, although you can play with the config file as necessary. Change the path names to your own, since all of the uploaded ones are my own absolute paths. 

The code is intended to help someone merge two hmmalign results. That is, given a backbone alignment on `{S1, S2, S3, S4}` and two query sequences `x` and `y`, if we build an HMM on `{S1, S2} and another on `{S3, S4}` using HMMER, then align `x` to `{S1, S2}` and align `y$ to `{S3, S4}`, we would like to be able to create a final alignment with `{S1, S2, S3, S4, x, y}`. 

query_x.txt and query_y.txt show the two query sequences. I've also provided two scripts `run_gap.sh` and `run_nogap.sh` to illustrate how to generate the other transient input files necessary. Note that I have both `s1_subset.txt`, `s2_subset.txt` and a second pair `s1_subset2.txt` and `s2_subset2.txt` to illustrate the difference in outputs if you include gaps in the subset sequences passed to the SEPP code. **In particular, you want to follow the nogaps pipeline in order to get a final alignment.**
