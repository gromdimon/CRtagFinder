# File: bioinformatics_utils.py (Add this function to the module)

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import logging

def make_labels_for_ncbi_from_hmmer(hmmer_output_path, output_protein_path):
    """
    Reads hmmer output (EMBL UniProt labels) and makes a list of labels for NCBI.
    :param hmmer_output_path: Path to the HMMER output file 'download.fa'.
    :param output_protein_path: Path to the output file for processed proteins.
    :return: Tuple of two lists - NCBI labels and processed IDs.
    """
    ncbi, list_of_ids, prot_ids, processed = [], [], [], []
    try:
        with open(hmmer_output_path, "r") as download_fa, open(output_protein_path, "w") as output_prots:
            strings = download_fa.read().splitlines()
            for string in strings:
                if string.startswith(">") and "/" in string:
                    prot_ids.append(string[1 : string.find("/")])
                elif string.startswith(">") and "/" not in string:
                    prot_ids.append(string[1:])
                elif len(prot_ids) >= 20:
                    list_of_ids.append(prot_ids)
                    prot_ids = []
            list_of_ids.append(prot_ids)

            # Convert labels from Uniprot to NCBI and build uniprot-embl dictionary
            for ids in list_of_ids:
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                id_converter = session.get(
                    f"https://www.uniprot.org/uploadlists/?"
                    f"&from=ACC&to=EMBL&format=tab&api_key=YOUR_API_KEY&query={','.join(ids)}"
                )
                raw_ids = id_converter.text.splitlines()
                for id in raw_ids[1:]:
                    logging.info(id)
                    uniprot, embl = id.split("\t")
                    if uniprot not in processed:
                        ncbi.append(embl)
                        processed.append(uniprot)

            # Write new proteins file with only converted proteins
            write_prot = False
            for string in strings:
                if string.startswith(">"):
                    prot_id = string[1 : string.find("/")] if "/" in string else string[1:]
                    if prot_id in processed:
                        output_prots.write(f'>{prot_id}\n')
                        write_prot = True
                    else:
                        write_prot = False
                else:
                    if write_prot:
                        output_prots.write(f"{string}\n")

        return ncbi, processed
    except Exception as e:
        logging.error(f"Error in make_labels_for_ncbi_from_hmmer: {e}")
        return [], []
