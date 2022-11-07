# CRtagFinder

# Database Query Tool (DQT)

## Table of Contents
* [General Overview](#General-Overview)
* [Prerequisites](#Prerequisites)
* [Skript Execution](#Skript Execution)
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
After cloning the CRtagFinder repository you can run quick skript, but also debug some other files.
```
python3 CRTagExtractor.py
```

### Results
After all you will have many files in different formats, with different information etc. For purposes of SigmoID we handled special final files
"final_r2.txt" and "final_r4.txt". They are made in special table for [ProtDnaKorr](http://bioinf.fbb.msu.ru/Prot-DNA-Korr/) application. This app made
special heatmaps, that illustrated correlations. With help of it we constructed CR-tags and protein database.


## Additional Information

Should be ready for CPU consumption, Internet stability and time! This script is not well-optimised for big data, but works actually with it..
So be ready!


