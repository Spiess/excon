import argparse
import csv
import os
import sys

from PyPDF2 import PdfFileMerger


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('groups_file', help="CSV file containing group member names. Each row is a group.")
    parser.add_argument('source_directory', help="Source directory containing subdirectories with original documents.")
    parser.add_argument('target_directory', help="Directory to write results to.")
    parser.add_argument('exercise', help="The name or number of the exercise.")

    args = parser.parse_args()

    groups_file = args.groups_file
    source = args.source_directory
    target = args.target_directory
    exercise = args.exercise

    groups = []

    with open(groups_file) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            groups.append(row)

    team_dirs = [d for d in os.listdir(source) if os.path.isdir(os.path.join(source, d))]
    dirs = [(d, sd) for d in team_dirs for sd in os.listdir(os.path.join(source, d)) if
            os.path.isdir(os.path.join(source, d, sd)) and os.listdir(os.path.join(source, d, sd))]

    # TODO: Check that no two students have the same last name

    hand_ins = [None] * len(groups)
    for d, s in dirs:
        lastname = s.split('_')[0]
        i = find_group(groups, lastname)
        if i == -1:
            print(f'ERROR: Name not found "{lastname}"!', file=sys.stderr)
            continue
        if hand_ins[i]:
            print(f'ERROR: Too many hand-ins for group {i} ("{lastname}")!', file=sys.stderr)
            continue
        directory = os.path.join(source, d, s)
        pdfs = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.pdf')]
        if len(pdfs) != 1:
            print(f'ERROR: Incorrect number of PDFs found in "{directory}"!', file=sys.stderr)
            continue
        hand_ins[i] = os.path.join(directory, pdfs[0])

    merger = PdfFileMerger(strict=False)
    for i, pdf in enumerate(hand_ins):
        if not pdf:
            print(f'ERROR: No hand-in for group {i} - {groups[i]}!', file=sys.stderr)
            continue
        merger.append(pdf)

    os.makedirs(target, exist_ok=True)
    merger.write(os.path.join(target, f'{exercise} All.pdf'))
    merger.close()


def find_group(groups, lastname):
    for i, group in enumerate(groups):
        for name in group:
            if name.endswith(lastname):
                return i
    return -1


if __name__ == '__main__':
    main()
