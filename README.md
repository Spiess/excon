# excon
Python exercise sheet converter to concatenate multiple exercise sheets into a single PDF and split them up again.

A row in the group file corresponds to a single team therefore the group file should contain *num_groups* rows with *group_size* names. A group may also consist of a single person.

Example groups file `groups.csv`:
```
First Last,Maxine Muster,
Otto Normalverbraucher,John Appleseed,Alain Thüring
Kerkylas of Andros,
Anakin Skywalker,Leia Organa,
```
where the first row can also be skipped.

## Setup
The only required setup is to install PyPDF2 into the Python environment:
```bash
pip install PyPDF2
```

## Code usage
```bash
python3 excon.py [mode] [groups_file] [source_directory] [target_directory] 
```
* [mode] a) ***split*** or b) ***merge***
* [groups_file] a) and b) path to csv file
* [source_directory] <br> a) and b) path to the directory containing the downloaded submission 
* [target_directory] <br> a) filepath where the merged pdf file should be created <br>b) same path as in a) where the merged pdf file is located. The split pdf files are also stored there.

## A) Instructions for concatenating all pdf files into a single
1. Create a subdirectory for the current exercise (e.g *./ex1*).
2. Create another subdirectory (e.g *./ex1/source*) and place the downloaded group submissions from ADAM in this directory.
3. By executing the code in *split* mode, the script creates a file *"[exercise_num] All.pdf"* in the target directory.

### Split example for exercise 1:

```bash
python3 excon.py merge ./ex1/ex1-groups.csv ./ex1/source ./ex1/target 1
```

This creates the merged file *./ex1/target/1 All.pdf*

After A), your project directory may look like:

```
excon
│   README.md
│   excon.py   
└───ex1
│   │   
│   └───source
│   │   │   Team XXXX
│   │   │   Team XXXY
│   │   │   Team XXXZ
│   │   │   ...
│   │
│   └───target
│       │   1 All.pdf
```

## B) Instructions for splitting the merged and corrected pdf
1. Point to the same source directory as in A) where the downloaded posts are located. 
2. Point to the same target directory as in A). The merged and corrected pdf file must have the same name (*"[exercise_num] All.pdf"*) as the file created in A). 
3. The script splits (*"[exercise_num] All.pdf"*) into separate files for each group (e.g. *./ex1/target/1 Skywalker Organa*) in the target directory.

### Merge example  for exercise 1:
```bash
python3 excon.py merge ./ex1/ex1-groups.csv ./ex1/source ./ex1/target 1
```

After B) your project directory may look like:

```
excon
│   README.md
│   excon.py   
└───ex1
│   │   
│   └───source
│   │   │   Team XXXX
│   │   │   Team XXXY
│   │   │   Team XXXZ
│   │   │   ...
│   │
│   └───target
│       │   1 All.pdf
│       │   1 Normalverbraucher Appleseed Thüring.pdf
│       │   1 Andros.pdf
│       │   1 Skywalker Organa.pdf
│       │   ...
```
