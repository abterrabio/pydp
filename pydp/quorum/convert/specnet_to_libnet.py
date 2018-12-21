import argparse
from pyteomics import mgf
import sys
import logging

MZ_PRECISION = 0.01
def check_mz(mz, omz, node_id, oidx):
    if abs(float(mz) - omz) > MZ_PRECISION:
        logging.error("Mismapping: {0} {1} are off. Network analysis node {2} is inconsistent with spectral library index {3}.".format(mz, omz, node_id, oidx))
        sys.exit(-1)

def convert(args, out=sys.stdout):
    """Remaps the nodes from a network analysis (sorted by pepmass) to the same order as the spectral library."""
    with mgf.read(args.lib_mgf) as reader:
        spectra = list(sorted((sp['params']['pepmass'][0],oidx) for oidx, sp in enumerate(reader)))

    node_fmt = "{0}l{1:010d}".format
    with open(args.edges_tsv) as f:
        for line in f:
            if line.startswith('#'):
                out.write(line)
                continue
            tokens = line.split('\t')
            s_mz, s_idx = tokens[0].split('-')
            s_omz, s_oidx = spectra[int(s_idx)]
            check_mz(s_mz, s_omz, tokens[0], s_oidx)

            t_mz, t_idx = tokens[1].split('-')
            t_omz, t_oidx = spectra[int(t_idx)]
            check_mz(t_mz, t_omz, tokens[1], t_oidx)

            out.write('\t'.join([node_fmt(s_mz, s_oidx), node_fmt(t_mz, t_oidx), 'll',] + tokens[3:]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Converts a network analysis of a spectral library with unique compounds to a static library edges file.")
    parser.add_argument("lib_mgf", type=str, help="mgf file containing library spectra")
    parser.add_argument("edges_tsv", type=str, help="edges file produced by network analysis")
    parser.add_argument("-o", dest="prefix", type=str, default=None, help="outputs edges file to `prefix.edges.tsv` by default outputs to stdout.")
    args = parser.parse_args()
    if args.prefix is None:
        convert(args)
    else:
        with open("{0}.edges.tsv".format(args.prefix), 'w') as f:
            convert(args, f)
