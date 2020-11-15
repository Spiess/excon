import argparse
import csv
import os
import sys

from PyPDF2 import PdfFileMerger

SPECIAL_REPLACEMENTS = [
    ('Ä', 'Ae'),
    ('Ö', 'Oe'),
    ('Ü', 'Ue'),
    ('ä', 'ae'),
    ('ö', 'oe'),
    ('ü', 'ue')
]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('groups_file', help="CSV file containing group member names. Each row is a group.")
    parser.add_argument('source_directory', help="Source directory containing subdirectories with original documents.")
    parser.add_argument('target_directory', help="Directory to write results to.")
    parser.add_argument('exercise', help="The name or number of the exercise.")
    parser.add_argument('--strict', help="Use strict mode for PDF file merging.", action='store_true')
    parser.add_argument('--ignore-error', help="Merge found PDFs even if errors occur.", action='store_true')

    args = parser.parse_args()

    groups_file = args.groups_file
    source = args.source_directory
    target = args.target_directory
    exercise = args.exercise
    strict = args.strict
    ignore_error = args.ignore_error

    groups = []

    with open(groups_file) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            groups.append([name for name in row if name])

    # Expects source directory to be structured as: source dir/Team dir/Lastname_Firstname_email_number dir/hand-in.pdf
    team_dirs = [d for d in os.listdir(source) if os.path.isdir(os.path.join(source, d))]
    dirs = [(d, sd) for d in team_dirs for sd in os.listdir(os.path.join(source, d)) if
            os.path.isdir(os.path.join(source, d, sd)) and os.listdir(os.path.join(source, d, sd))]

    # Check that no two students have the same last name
    last_names = [name.split()[-1] for group in groups for name in group]
    if len(last_names) != len(set(last_names)):
        print('ERROR: Two students appear to have the same last name, which is not supported in this version of excon!',
              file=sys.stderr)
        exit(1)

    error = False

    hand_ins = [''] * len(groups)
    for d, s in dirs:
        lastname = s.split('_')[0]
        i = find_group(groups, lastname)
        if i == -1:
            print(f'ERROR: Name not found "{lastname}"!', file=sys.stderr)
            error = True
            continue
        if hand_ins[i]:
            print(f'ERROR: Too many hand-ins for group {i} ("{lastname}")!', file=sys.stderr)
            error = True
            continue
        directory = os.path.join(source, d, s)
        pdfs = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.pdf')]
        if len(pdfs) != 1:
            print(f'ERROR: Incorrect number of PDFs found in "{directory}"!', file=sys.stderr)
            error = True
            continue
        hand_ins[i] = os.path.join(directory, pdfs[0])

    merger = PdfFileMerger(strict=strict)
    for i, pdf in enumerate(hand_ins):
        if not pdf:
            print(f'ERROR: No hand-in for group {i} - {groups[i]}!', file=sys.stderr)
            error = True
            continue
        merger.append(pdf)

    if not ignore_error and error:
        print('Errors have occurred and no merged PDF was written. Correct errors manually or use the "--ignore-error" '
              'flag to proceed.')
        return

    os.makedirs(target, exist_ok=True)
    target_file = os.path.join(target, f'{exercise} All.pdf')
    merger.write(target_file)
    merger.close()
    print(f'Merged PDF written to {target_file}.')


def find_group(groups, lastname):
    for i, group in enumerate(groups):
        for name in group:
            if replace_special(name).endswith(lastname):
                return i
    return -1


def replace_special(s):
    for character, replacement in SPECIAL_REPLACEMENTS:
        s = s.replace(character, replacement)
    return s


if __name__ == '__main__':
    main()
