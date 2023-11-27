# CRtagFinder

## Table of Contents
* [General Overview](#General-Overview)
* [Prerequisites](#Prerequisites)
* [Skript Execution](#Skript-Execution)
* [Additional Information](#Additional-Information)

## General Overview 
CRTagFinder is an automated pipeline for finding critical residues (CR) in sigma-factors proteins. This skript is essential for semi-automated pipeline
of bacterial genomes annotation in [SigmoID](https://github.com/nikolaichik/SigmoID) distributive. One of the essential prerequisites for this pipeline
is custom database with Transkription Factors and their critical residues tags. CR-tag is an order of positions of amino-acid residues within DNA binding
domain, which direktly contact DNA bases. For the construction of database the data from this script was used.

## Prerequisites
For running this script some third-side packages and applications are required. They are: 
-[Biopython](https://biopython.org/)
-[HMMER](http://hmmer.org/)
HMMER is a complete application, that has to be installed and setted up. See hints [here](http://hmmer.org/download.html).

### Input Files

You also need a "download.fa" file in the directory where the script is located. This file should consist of protein sequences in fasta format with
UniProt identificators.

Example:
```
>D0LGP0_HALO1/3-191
RRERALIRKLRDRDERAFRELVTQFGDRIFNLTFRMLGSREEAEDISQEVFITVFKSIDS
FRGDAKFSTWMYRIAVNHCKNRIKYLARRHDRSRDEYDDMSGQQQAAGATAVPSTPARPD
LQLEGVQLEQIMQRCIASLDEEHRVLIVLRDIEDLSYEEICTITNLPTGTVKSRLHRARL
ALRKKMLTK
>A0A5B8XTY0_9DELT/1-188
MSLSDRKLVRNLRRRDEDAFRELVRVYQHRVFNIVYRILGDREEAEDVAQEVFVAIFKHI
DSFRGDAKFSTWVYRIATNQARNRLKYHARRHRRDHQNYEDAPESAHQDSDFAGTIPQPE
DAVLGRELEKIIQEGLAELGEIHRTIIVLRDVEHLSYQEIAEIVELPEGTVKSRLFRARV
ALKEYVEK
>Q2IIH1_ANADE/32-211
AWTRSAARGDRQAFSRLVDLHKRTVFALCVRLLRDQDEAQDAAQEAFARAYASLAAFDPS
QPFAPWLLRIARNHCLDVIRRRLPQAQRVELDAAPEDGAPRDLADPDAPRGDDALERREL
ARTLEAAVAALPANYREVVHLFHVEHLSYKEIAAAMDVPIGTVMTWLHRARARLKATLDA
```

## Skript Execution
### Quick Mode:
You have to copy only script itself [CRTagExtractor](https://github.com/gromdimon/CRtagFinder/blob/main/CRTagExtractor.py) and move 'download.fa' file in
the same directory. The execusion will be performed by running skript with python command:
```
python3 CRTagExtractor.py
```

### Developer mode:
After cloning the CRtagFinder repository you can run quick skript, but also debug some other files. The real pipeline is in `CRtagFinder` folder.

**1. `bioinformatics_utils.py`**

This module contains functions specific to bioinformatics tasks. It includes methods for parsing DNA sequences, finding gene locations in genomes, and other sequence-related operations.

Key Functions:
- `make_labels_for_ncbi_from_hmmer`: Converts EMBL UniProt labels from HMMER output into NCBI labels.
- `find_places`: Extracts locations of proteins in a genome from a GenBank file.
- `parce_dna`: Parses DNA sequences from NCBI based on given genome locations.

**2. `config.py`**

Central configuration module that stores global settings, API keys, file paths, and URLs. This module simplifies the management of constants used across the application.

Contains:
- API keys (e.g., NCBI API key).
- File paths for input and output data.
- URLs for downloading HMM models.
- Global settings like the sigma factor.

**3. `hmm_analysis.py`**

Focuses on tasks related to Hidden Markov Model (HMM) analysis, particularly for protein and DNA sequences.

Key Functions:
- `find_regions`: Analyzes protein and DNA sequences using HMM.
- `protdnakorr_adaptation`: Adapts data for subsequent analysis steps.

**4. `net_file_utils.py`**

A utility module for network requests and file operations. It includes functions to handle downloading files, creating sessions with retry capabilities, and basic file reading and writing.

Key Functions:
- `create_session_with_retries`: Creates a requests session with retry capabilities.
- `download_file`: Downloads a file from a given URL.
- `read_file`, `write_file`, `append_to_file`: Utility functions for file operations.

**5. `main.py`**

The entry point of the application. It orchestrates the workflow by calling functions from other modules in the required sequence. The `main.py` script manages the overall data processing pipeline, ensuring that each step is executed in order and the data is passed correctly between functions.


### Results
After all you will have many files in different formats, with different information etc. For purposes of SigmoID we handled special final files
"final_r2.txt" and "final_r4.txt". They are made in special table for [ProtDnaKorr](http://bioinf.fbb.msu.ru/Prot-DNA-Korr/) application. This app made
special heatmaps, that illustrated correlations. With help of it we constructed CR-tags and protein database.


## Additional Information

Should be ready for CPU consumption, Internet stability and time! This script is not well-optimised for big data, but works actually with it..
So be ready!

## Usage

1. Ensure all required Python packages are installed.
2. Set up the `config.py` module with the correct API keys, file paths, and other configurations.
3. Execute `main.py` to run the pipeline.

## Requirements

- Python 3.x
- Biopython
- Requests
- Other dependencies as required by the specific functions within the modules.
