#!/bin/bash

hmmbuild --informat afa --dna s1_hmm_gaps s1_subset.txt

hmmbuild --informat afa --dna s2_hmm_gaps s2_subset.txt

hmmalign --allcol --dna s1_hmm_gaps query_x.txt > s1_query_gaps.aln

hmmalign --allcol --dna s2_hmm_gaps query_y.txt > s2_query_gaps.aln

