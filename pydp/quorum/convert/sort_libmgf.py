import argparse
from pyteomics import mgf
import sys
import logging

def convert(args, out=sys.stdout):
    """Outputs spectral library sorted by mass."""
    with mgf.read(args.lib_mgf) as reader:
        mgf.write((s for _,_,s in sorted((sp['params']['pepmass'][0],oidx,sp) for oidx, sp in enumerate(reader) if sp['m/z array'].shape[0] >= args.min_peak_count)), output=out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sorts a mgf file by mass and removes spectra with too few peaks.")
    parser.add_argument("lib_mgf", type=str, help="mgf file containing unsorted library spectra")
    parser.add_argument("-p", dest="min_peak_count", type=int, default=3, help="minimum number of peaks for spectra, (default: 3).")
    parser.add_argument("-o", dest="prefix", type=str, default=None, help="outputs mgf file to `prefix.mgf` by default outputs to stdout.")
    args = parser.parse_args()
    if args.prefix is None:
        convert(args)
    else:
        with open("{0}.mgf".format(args.prefix), 'w') as f:
            convert(args, f)
