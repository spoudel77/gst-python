from Bio import SeqIO

import argparse
 # remove > if present anywhere else besides the beginning of line
def readFastString(filename):
    with open(filename) as file:
        return file.read().split('>')[1:]

def readFastEntry(filename):
    return[seq.partition('\n') for seq in readFastString(filename)]

def readFastseq (filename):
    return [[seq[0][0:], seq[2].replace('\n','')] for seq in readFastEntry(filename)]


# print list1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert multiple files of multi-line fasta into two-line fasta format')
    parser.add_argument('-i',type=str,dest='inf',required=True,help="Input file")
    parser.add_argument('-o',type=str,dest='outf',required=True,help="Ouput file")
    args = parser.parse_args()
    print args
    list1 = readFastseq(args.inf)
    for x in list1:
        # print x[0]
        with open(args.outf, 'a') as g:
            
            g.write('>'+x[0].strip()+"\n"+x[1].strip()+'\n')
            #g.write('>decoy_'+x[0].strip()+"\n"+x[1].strip()[::-1]+"\n")
