# CRtagFinder
CRTagFinder is an automated pipeline for finding critical residues (CR) in sigma-factors proteins.
Normal description and better code will be provided soon.

# Database Query Tool (DQT)

## Table of Contents
* [Workflow Overview](#Workflow-Overview)
* [Required Files](#Required-Files)
* [Workflow Execution](#Workflow-Execution)
* [Adding Custom Databases](#Adding-Custom-Databases)
* [Additional Information](#Additional-Information)

## Workflow Overview 
The Databse Query Tool is used to compare the contents of the reference databases used by various taxonomic classification tools. Specifically, since NCBI taxonomy is constantly being updated and different taxonomic classification tools use different databases, not all tools have the same reference organisms in their database. Thus, comparing outputs from one tool to another requires accounting for differences in the presence of organisms in their respective reference databases. If a taxonomic classification tool does not report an expected species in a metagenome, the DQT allows users to quickly query whether or not that species was present in the tool's reference database. The DQT allows the user to input one or more NCBI taxonomy IDs (taxids) and output a list of the databases that contain that taxid or its ancestor. While taxons from any level can be queried, this tool was specifically designed to work with species-level taxons. 

![](https://github.com/signaturescience/metagenomics-wiki/blob/master/documentation/figures/DQT%20v1.png)

## Required Files
If you have not already, you will need to clone the MetScale repository and activate your `metscale` environment (see [Install](https://github.com/signaturescience/metscale/wiki/02.-Install)) before proceeding:

```sh
[user@localhost ~]$ source activate metscale 

(metscale)[user@localhost ~]$ cd metscale/scripts

```

### Input Files

If you ran the MetScale installation correctly, the following files and directories should be present in the `metscale/scripts` directory.

## Workflow Execution
![](https://github.com/signaturescience/metscale/blob/master/scripts/DQT%20(Hackathon%202022).png)

### Quick Start:
After cloning the MetScale repository, some configuration is necessary before use. It can be done automatically using default settings by running the command:
```
python3 query_tool.py --setup
```
That will populate the setting `working_folder` in the default config file with the home folder of the DQT. Following that, the tool should be ready for use.

### Detailed Settings
The `--setup` command will automatically set the three important paths the DQT needs to run:
* 1) The repository of taxon coverage information for the various MetScale tools
* 2) The full reference taxonomy maintained by NCBI. 
* 3) The working folder for any outputs that are provided. 

## Usage 

### Taxon ID Querying

All RefSeq versions up to v98 can be included in the query by adding the flag `--all_refseq_versions`. 

#### Details & Example
 will run for only this taxon. Additionally, the output report will have a slightly different format than for multiple IDs.

## Output
To understand how to interpret the output of the DQT we will use the example query from the previous section:

## Adding Custom Databases

If a database of interest is not currently present in the DQT you can easily add it to the pool! A mock database `example_db.txt` is included with MetScale and we will use this file to demonstrate how to add a database.

### Database Format
The database must be formatted as follows:

### Adding The Database

The DQT uses a configuration file `dbqt_config` to organize databate inclusion. If you ran the DQT `--setup` your config file should look like:

### Inspection and Import
Now that we have included all our information in the config file, we will check to verify the DQT recognizes our new database. We will run the inspection flag `-CMO` to do this.
```
(metscale) :~$ python3 query_tool.py -BCD
Summary of sources to be imported: (count = 1)
   example      /path/to/metscale/scripts/databases/example_db.txt
[query_tool.py (1551)] INFO: Containment Dictionary Summary (all_refseq = False)
   ***
    # Databases: 106 (98 RefSeq, 8 other)
  Latest RefSeq: v98

Main Databases:
 Database Name                        # Taxa  Date Parsed
 ---------------------------------  --------  --------------------
 minikraken_20171019_8GB               10624  2020-02-24 15:56:01
 minikraken2_v2_8GB_201904_UPDATE      21112  2020-02-24 15:56:01
 kaiju_db_nr_euk                      224818  2020-02-24 15:56:01
 NCBI_nucl_wgs                         74902  2020-04-11 14:16:57
 NCBI_nucl_gb                        1893626  2020-04-11 14:20:05
 MTSV_Oct-28-2019                      24422  2020-05-19 02:28:52
 metaphlan3                            13519  2021-07-23 08:46:51
 example                                   7  2021-08-04 09:21:15
 RefSeq_v98                            98406  2020-02-24 15:56:00


[query_tool.py (1110)] INFO: Saving containment dictionary to /path/to/metscale/scripts/containment_dict.json
```
You should see the above output now displaying the new pool of databases in the DQT. Our `example` database is there! The process is now complete. You can replicate all these steps with as many custom databases as you would like. 

## Additional Information

A complete list of the commands and options is available using the `--help` flag at the command line:

```
python3 query_tool.py --help
```

### Logging Options:
Options related to how much information the program prints while running:
