#!/usr/bin/env python3

#script for single program testing

import argparse
import filecmp
import os
from tempfile import gettempdir

parser = argparse.ArgumentParser(description='Get prog dir.')
parser.add_argument('-d', '--dir', help='directory with prog and tests')
args = parser.parse_args()


num_of_tests = len(os.listdir(os.path.join(args.dir, 'tests'))) // 2

for i in range(1, num_of_tests + 1):
	program_file = os.path.join(args.dir, 'prog.py')
	input_file = os.path.join(args.dir, 'tests', f'{i}.in')
	gt_file = os.path.join(args.dir, 'tests', f'{i}.out')
	tmp_file = os.path.join(gettempdir(), 'output.out')
	
	os.system(f'python3 {program_file} < {input_file} > {tmp_file}')
	
	print('Test #{}: {}'.format(i, 'OK' if filecmp.cmp(gt_file, tmp_file) else 'NOT OK'))