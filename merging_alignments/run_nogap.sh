#!/bin/bash

hmmbuild --informat afa --dna s1_hmm_nogaps s1_subset2.txt

hmmbuild --informat afa --dna s2_hmm_nogaps s2_subset2.txt

hmmalign --allcol --dna s1_hmm_nogaps query_x.txt > s1_query_nogaps.aln

hmmalign --allcol --dna s2_hmm_nogaps query_y.txt > s2_query_nogaps.aln

