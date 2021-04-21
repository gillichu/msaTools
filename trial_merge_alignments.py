'''
Created on Apr 10, 2021

@author: gillichu
'''
from sepp.alignment import MutableAlignment, ExtendedAlignment
from sepp.exhaustive import JoinAlignJobs
from sepp.problem import SeppProblem
import glob

job_joiner = JoinAlignJobs
flag = 'gaps'

# Note that extension.txt is a file I got by writing an additional logfile in <problem.py>
# If you'd like the same, add "ap_alg.write_to_path("/Users/gillianchu/warnow/bin/gitrepos/smirarab-sepp-17a33aa/trial/extension.txt")"
# to the "read_extendend_alignment_and_relabel_columns()" of the SeppProblem class.
# Make sure to do this before the last line relabeling columns, since that's usually the line that errors. 
# backbone alignment 
original_backbone_file = ('/Users/gillianchu/warnow/bin/gitrepos/smirarab-sepp-17a33aa/trial/orig_backbone.txt')
new_backbone_file = "new_backbone_file.txt"

with open(original_backbone_file, "r") as reader:
    with open(new_backbone_file, "w+") as writer:
        for line in reader.readlines():
            if line[0] == ">":
                writer.write(line.upper())
            else:
                writer.write(line)

original_backbone = MutableAlignment()
done = original_backbone.read_filepath(new_backbone_file) 

# all query sequences
original_frag_file = ('/Users/gillianchu/warnow/bin/gitrepos/smirarab-sepp-17a33aa/trial/all_query.txt')
original_frag = MutableAlignment()
done = original_frag.read_filepath(original_frag_file)

# First build extended alignment on entire fragment set
extendedAlignment = ExtendedAlignment(original_frag.get_sequence_names())
dir = '/Users/gillianchu/warnow/bin/gitrepos/smirarab-sepp-17a33aa/trial/'

for a in [1, 2]:
    a = str(a)
    print("Working on HMM %s\n" % a)

    # query sequences
    aligned_files = glob.glob(str(dir)+'s'+str(a)+'_query.aln')
    if a == '1':
        sequence_files = glob.glob(str(dir)+'query_x.txt')
    elif a == '2':
        sequence_files = glob.glob(str(dir)+'query_y.txt')

    # sequences your hmm was trained on. Ensure you didn't just take the backbone alignment and 
    # restrict the subset of sequences. This file must not have any gaps in it. 
    if flag == "gaps":
        base_alignment_file = str(dir)+'s' + str(a) + '_subset.txt'
    else:
        base_alignment_file = str(dir)+'s' + str(a) + '_subset2.txt'
    base_alignment = MutableAlignment()

    print("aligned_files:", aligned_files)
    print("sequence_files:", sequence_files)
    print("base_alignment_file :", base_alignment_file)

    done = base_alignment.read_filepath(base_alignment_file) # [0]
    subbackbone = original_backbone.get_soft_sub_alignment(
        base_alignment.get_sequence_names())
    print("Orig alignment sequences: ", original_backbone.get_sequence_names())
    print("Base alignment sequences: ", base_alignment.get_sequence_names())

    print("num base alignment seqs: ", len(base_alignment.get_sequence_names()))

    frags = MutableAlignment()
    sequence_names = []
    for file in sequence_files:
        seq = MutableAlignment()
        done = seq.read_filepath(file)
        print('query sequence names:', seq.get_sequence_names())
        print("query sequence length:", seq.get_length())
        done = sequence_names.extend(seq.get_sequence_names())
        for name, seq in seq.items():
            frags[name] = seq.upper()

    problem = SeppProblem(sequence_names)
    problem.set_subalignment(subbackbone)

    # constructs sub-base-alignment from the full alignment, delete all gaps
    mut_subalg = problem.subalignment.get_mutable_alignment()
    remaining_cols = mut_subalg.delete_all_gap()
    problem.annotations["ref.alignment.columns"] = remaining_cols
    print("num remaining_cols: ", len(remaining_cols))
    problem.fragments = frags

    ap_alg = problem.read_extendend_alignment_and_relabel_columns(
        base_alignment_file, aligned_files)
    extendedAlignment.merge_in(ap_alg, convert_to_string=True)

extendedAlignment.write_to_path(dir + "merged_alignment_unmasked_" + flag + ".fasta")
extendedAlignment.remove_insertion_columns()
extendedAlignment.write_to_path(dir + "merged_alignment_masked_" + flag + ".fasta")
