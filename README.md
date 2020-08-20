# BOLDigger-commandline
BOLDigger as a command-line tool for easy implementation into bioinformatic pipelines.

Before using please check that you have updated to the latest version of BOLDigger since BOLDigger-cline heavily relies on the current code of BOLDigger.

For a detailed explanation of the different functions BOLDigger offers please visit:
https://github.com/DominikBuchner/BOLDigger

## Installation
BOLDigger-commandline requires Python version 3.6 or higher and can be easily installed by using pip in any command line:

`pip install boldigger-cline`

will install BOLDigger-commandline as well as all needed dependencies.

To update BOLDigger-commandline type:

`pip install --upgrade boldigger-cline`

## How to cite

Buchner D, Leese F (2020) BOLDigger – a Python package to identify and organise sequences with the Barcode of Life Data systems. Metabarcoding and Metagenomics 4: e53535. https://doi.org/10.3897/mbmg.4.53535

## Usage

BOLDigger commandline offers all functions of BOLDigger as a command line tool.

For documentation on how to use type:

`boldigger-cline -h`

Returns:

```
usage: boldigger-cline [-h] [--version]
                       {ie_coi,ie_its,ie_rbcl,add_metadata,first_hit,jamp_hit,digger_hit}
                       ...

BOLDigger as a command line tool, https://github.com/DominikBuchner/BOLDigger-

commandline

positional arguments:
  {ie_coi,ie_its,ie_rbcl,add_metadata,first_hit,jamp_hit,digger_hit}
    ie_coi              COI identification engine
    ie_its              ITS identification engine
    ie_rbcl             rbcl identification engine
    add_metadata        additional data download
    first_hit           use the first hit as top hit
    jamp_hit            determine the top hit with the JAMP method
    digger_hit          determine the top hit with the BOLDigger method

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

The help function also works for all sub-functions of BOLDigger-commandline:

`boldigger-cline ie_coi -h`

Returns:

```
usage: boldigger-cline ie_coi [-h]
                              username password fasta_path output_folder

                              [batch_size]

positional arguments:
  username       Username for boldsystems login
  password       Password for boldsystems login
  fasta_path     Path to the fasta file to be blasted
  output_folder  Path to the output folder
  batch_size     Batch size to be blasted.

optional arguments:
  -h, --help     show this help message and exit
```

### Identification engine - Example usage
To run the identification engine for COI type:

`boldigger-cline ie_coi username password fasta_path output_folder [batch size](optional)`

### Additional data download and top hit determination
All other function of BOLDigger commandline just need a filepath to the BOLDResult file as an argument.


# TODO
- Write manual
- Publish on PyPi
