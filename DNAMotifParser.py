import random
import requests
from Bio import SeqIO
from Bio.Seq import Seq
from subprocess import Popen, PIPE
import re
import wget
import pathlib

def make_labels_for_ncbi_from_hmmer():
    '''
    The function converts indexes from Embl to Ncbi format
    :input: download.fa
    :return: labels_for_ncbi
    '''
    with open('download.fa', 'r') as download_fa:
        strings = download_fa.read().splitlines()
        ncbi = []
        list_of_ids = []
        prot_ids = []
        for string in strings:
            if string.startswith('>') and '/' in string:
                end = string.find('/')
                prot_ids.append(string[1:end])
            elif string.startswith('>')and '/' not in string:
                prot_ids.append(string[1:])
            elif len(prot_ids) >= 30:
                list_of_ids.append(prot_ids)
                prot_ids = []
        list_of_ids.append(prot_ids)

        for ids in list_of_ids:
            id_converter = requests.get(
                f"https://www.uniprot.org/uploadlists/?"
                f"&from=ACC&to=EMBL&format=tab&query={','.join(ids)}")
            raw_ids = id_converter.text.splitlines()

            for id in raw_ids[1:]:
               uniprot, embl = id.split('\t')
               if uniprot not in ncbi:
                    ncbi.append(embl)

    return ncbi


def find_positions(ncbi_labels):
    '''
    The function takes protein label, that are suitable with NCBI
    and performs finding protein gbk file
    :return: gb_prot.gbk
    '''
    with open('gb_prot.gbk', 'w') as pos_file:
        position = []
        for label in ncbi_labels:
            final_position = requests.get(
                f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
                f"efetch.fcgi?db=protein&rettype=gp&retmode=text&id={label}")
            position.append(final_position.text)

        pos_file.write('\n'.join(position))


def find_places():
    '''
    The function takes protein files and finds DNA places of this protein
    in genome of the organism, where the protein was found
    :return: dna_places_new.txt
    '''
    with open('gb_prot.gbk', 'r') as handle:
        places = []
        seq_records = SeqIO.parse(handle, 'genbank')
        for record in seq_records.records:
            for feature in record.features:
                if feature.type == 'CDS':
                    places.append(feature.qualifiers['coded_by'][0])

    return places


def parce_dna(places):
    """
    The function parces genomes by using information of positions of genes
    :return: dna_seq.fa
    """
    # list_of_places = [places[x:x + 100] for x in range(0, len(places), 30)]
    genomes_list = []
    # for places in list_of_places:
    for place in places:
        EntryID, coordinates = place.split(':')
        id = EntryID.replace('complement(', '')
        entryStart, entryEnd = coordinates.split('..')
        start = entryStart
        end = entryEnd
        if ')' in entryEnd:
            end = entryEnd.replace(')', '')
        dna = requests.get(
            f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=+{id}+&rettype=fasta&retmode=text&seq_start=+Str({start})+"&seq_stop="+Str({end})+DevInfo')
        genomes_list.append(dna.text)

    with open('dna_seq.fa', 'w') as dna_file:
        dna_file.write('\n'.join(genomes_list))


def install_files():
    directory_path = pathlib.Path(__file__).parent.resolve()

    try:
        with open('Sigma70_r2.hmm', 'r') as f:
            pass
    except IOError:
        Sigma70_r2 = "https://github.com/gromdimon/CRtagFinder/raw/main/Sigma70_r2.hmm"
        wget.download(Sigma70_r2, f'{directory_path}/Sigma70_r2.hmm')

    try:
        with open('Sigma70_r4.hmm', 'r') as f:
            pass
    except IOError:
        Sigma70_r4 = 'https://github.com/gromdimon/CRtagFinder/raw/main/Sigma70_r4.hmm'
        wget.download(Sigma70_r4, f'{directory_path}/Sigma70_r4.hmm')

    try:
        with open('AlgU.hmm', 'r') as f:
            pass
    except IOError:
        AlgU = 'https://github.com/gromdimon/CRtagFinder/raw/main/AlgU.hmm'
        wget.download(AlgU, f'{directory_path}/AlgU.hmm')


def find_regions():
    '''
    The function extracts from input download.fa and dna_seq.fa files
    r2 and r4 domens in protein sequence and dna promotor with -10 & -35 motifs
    :return:
    '''
    def parce_motifs():
        """
        The function uses HMM models for finding protein and DNA motifs
        :return:
        """
        process_prot_r2 = Popen(['hmmsearch', '-A', 'temp_protein_r2.txt', 'Sigma70_r2.hmm', 'temp_current_prot.fa'], stdout=PIPE,
                                stderr=PIPE)
        stdout_r2, stderr_r2 = process_prot_r2.communicate()
        process_prot_r4 = Popen(['hmmsearch', '-A', 'temp_protein_r4.txt', 'Sigma70_r4.hmm', 'temp_current_prot.fa'], stdout=PIPE,
                                stderr=PIPE)
        stdout_r4, stderr_r4 = process_prot_r4.communicate()
        process_dna_r2 = Popen(['nhmmer', '-o', 'temp_dna_r.txt', 'AlgU.hmm', 'temp_current_dna.fa'], stdout=PIPE, stderr=PIPE)
        dnaout_r, dnaerr_r = process_dna_r2.communicate()

        if stderr_r2 or stderr_r4 or dnaerr_r:
            return None
        return stdout_r2, stdout_r4, dnaout_r

    def check_values(stdout_r2):
        '''
        Checking if hmmer found anything
        :param stdout_r2:
        :return: True/False
        '''
        sp = stdout_r2.decode('utf-8')
        if '[No hits detected that satisfy reporting thresholds]' in sp:
            return False
        return True

    def byte_str_operating(protein_id, stdout_r2, stdout_r4, gene_id):
        '''
        Operating byte console output for extracting motifs
        '''
        protein_out_2 = stdout_r2.decode('utf-8')
        lines_r2 = protein_out_2.split(f'  {protein_id} ')
        protein_r2_domen = ''
        for line in lines_r2[2:]:
            line_spis = line.split(' ')
            if line_spis[1].isnumeric():
                protein_r2_domen += str(line_spis[2])
            else:
                protein_r2_domen += str(line_spis[1])

        protein_out_4 = stdout_r4.decode('utf-8')
        lines_r4 = protein_out_4.split(f'  {protein_id} ')
        protein_r4_domen = ''
        for line in lines_r4[2:]:
            line_spis = line.split(' ')
            if line_spis[1].isnumeric():
                protein_r2_domen += str(line_spis[2])
            else:
                protein_r4_domen += str(line_spis[1])

        with open('temp_dna_r.txt', 'r') as dna_out:
            dna_motif_list = []
            dna_r = dna_out.read().split('>>')
            for line in dna_r[1:]:
                line_spis = line.split(f'{gene_id}')
                line_mot = line_spis[2].split(' ')
                mot = line_mot[2]
                dna_motif_list.append(mot)

        return protein_r2_domen, protein_r4_domen, dna_motif_list

    def get_idseq(fasta):
        '''
        Making label + seq form faste file
        '''
        lines = fasta.split("\n")
        id = lines[0].split(" ")[0]
        seq = ''.join(lines[1:])

        return (id, seq)

    def lengthening_patterns(dna_motif, genome):
        '''
        Return extended motif
        '''
        # pattern = '......' + dna_motif + '......'
        # match_list = re.findall(pattern, genome, flags=re.DOTALL)
        # if match_list:
        #     match = match_list[0]
        # else:
        #     match = dna_motif

        one_line = genome.replace('\n', '')
        start_place = one_line.find(dna_motif)
        if start_place == -1:
            dna_forward = Seq(dna_motif)
            dna_reverse = dna_forward.reverse_complement()
            dna_reverse_line = str(dna_reverse)
            start_place = one_line.find(dna_reverse_line)
            if start_place == -1:
                return 'none'
            else:
                gene_line = one_line[start_place - 10:start_place + 50]
                gene_forward = Seq(gene_line)
                gene_reverse = gene_forward.reverse_complement()
                gene_reverse_line = str(gene_reverse)
                return gene_reverse_line
        gene_line = one_line[start_place - 10:start_place + 50]

        # output = []
        # output.append(match)
        # output.append(gene_line)

        return gene_line #output

    with open('dna_seq.fa', 'r') as dna, open('download.fa', 'r') as prot:
        dna_list = dna.read().split('>')
        prot_list = prot.read().split('>')
        genomes_list = list(map(get_idseq, dna_list[1:]))
        proteins_list = list(map(get_idseq, prot_list[1:]))

        with open('proteins_r2_for_align.fa', 'w') as prot_r2, open('proteins_r4_for_align.fa', 'w') as prot_r4,\
                open('dna_for_align.fa', 'w') as dna_r, open('dna_for_lengthening.fa', 'w') as leng_dna:
            for genome, protein in zip(genomes_list, proteins_list):
                gene_id, gene_seq = genome
                protein_id, protein_seq = protein

                with open('temp_current_prot.fa', 'w') as prot_file:
                    prot_file.write(f'> {protein_id}\n')
                    prot_file.write(protein_seq)

                with open('temp_current_dna.fa', 'w') as prot_file:
                    prot_file.write(f'> {gene_id}\n')
                    prot_file.write(gene_seq)

                if parce_motifs() != None:
                    stdout_r2, stdout_r4, dnaout_r = parce_motifs()
                else:
                    continue
                if check_values(stdout_r2) == False or check_values(dnaout_r) == False:
                    continue
                protein_r2, protein_r4, dna_r_list = byte_str_operating(protein_id, stdout_r2, stdout_r4, gene_id)

                # dna_motif_list = []
                gene_spis = []
                for dna_motif in dna_r_list:
                    # output = lengthening_patterns(dna_motif, gene_seq)
                    # match, gene_line = output[0], output[1]
                    gene_line = lengthening_patterns(dna_motif, gene_seq)
                    # dna_motif_list.append(match)
                    gene_spis.append(gene_line)

                prot_r2.write(f'>{protein_id}\n{protein_r2}\n')
                prot_r4.write(f'>{protein_id}\n{protein_r4}\n')
                for idx, motif in enumerate(dna_r_list):
                    dna_r.write(f'>{protein_id}_{idx}\n{motif}\n')
                # for idx, motif in enumerate(dna_motif_list):
                #     matches.write(f'>{protein_id}_{idx}\n{motif}\n')
                for idx, gene in enumerate(gene_spis):
                    leng_dna.write(f'>{protein_id}_{idx}\n{gene}\n')


def aligning_dna():
    process = Popen(['clustalw', '-INFILE=dna_for_align.fa', '-OUTPUT=FASTA', '-OUTFILE=aligned_dna.fa'],
                            stdout=PIPE,
                            stderr=PIPE)
    stdout_r2, stderr_r2 = process.communicate()
    if stderr_r2:
        return False
    else:
        return True


def lengthening():
    def get_idseq(fasta):
        lines = fasta.split("\n")
        raw_id = lines[0].split(" ")[0]
        id = raw_id  # [:raw_id.find('/')] + f'_{random.randint(100)}'
        seq = ''.join(lines[1:])
        return (id, seq)

    def lengthening_patterns(dna_motif, genome):
        pattern = dna_motif.replace('-', '.')
        match_list = re.findall(pattern, genome, flags=re.DOTALL)
        if match_list:
            match = match_list[0]
        else:
            match = dna_motif
        return match

    # Here also should be located aligned dna file
    with open('dna_for_lengthening.fa', 'r') as dna_find, open('aligned_dna.fa', 'r') as aligned_motifs, open(
            'lengthed_dna.fa', 'w') as output:
        gene_list = dna_find.read().split('>')
        motif_list = aligned_motifs.read().split('>')
        genomes_list = list(map(get_idseq, gene_list[1:]))
        patterns_list = list(map(get_idseq, motif_list[1:]))
        gene_dict = dict(genomes_list)

        for pattern in patterns_list:
            motifs_list = []
            pattern_id, pattern_seq = pattern
            pattern_id = pattern_id[:pattern_id.find('/' , pattern_id.find('/') + 1)]
            if not pattern_id in gene_dict:
                motifs_list.append(pattern_seq)
            else:
                gene = gene_dict[pattern_id]
                match = lengthening_patterns(pattern_seq, gene)
                if match != None:
                    motifs_list.append(match)

            for idx, motif in enumerate(motifs_list):
                output.write(f'>{pattern_id}_{idx}_{random.randint(1, 10)}\n{motif}\n')


def protdnakorr_adaptation():
    '''
    The function prepares data for ProtDnaKorr tool
    '''
    def return_idseq(fasta):
        lines = fasta.split("\n")
        id = lines[0].split(" ")[0]
        seq = ''.join(lines[1:])
        return (id, seq)

                                                                                              #dna_modified.fa
    with open('prot_r2_modified.fa', 'r') as r2, open('prot_r4_modified.fa', 'r') as r4, open('lengthed_dna_hrpl.fa', 'r') as r, open('final_r2.txt', 'w') as f2, open('final_r4.txt', 'w') as f4:  #
        f2.write('sequences.AA						sequences.DNA\n')
        f4.write('sequences.AA						sequences.DNA\n')
        dna_list = r.read().split('>')
        prot_list_2 = r2.read().split('>')
        prot_list_4 = r4.read().split('>')
        genomes_list = list(map(return_idseq, dna_list[1:]))
        proteins_list_2 = list(map(return_idseq, prot_list_2[1:]))
        proteins_list_4 = list(map(return_idseq, prot_list_4[1:]))

        for genome in genomes_list:
            for prot in proteins_list_2:
                if prot[0][:-7] in genome[0]:
                    f2.write(f'{prot[1]}\t{genome[1][-9:]}\n')

        for genome in genomes_list:
            for prot in proteins_list_4:
                if prot[0][:-8] in genome[0]:
                    f4.write(f'{prot[1]}\t{genome[1][:8]}\n')


# ncbi_labels = make_labels_for_ncbi_from_hmmer()
#
# find_positions(ncbi_labels)
#
# places = find_places()
#
# parce_dna(places)
#
# install_files()
#
# find_regions()
#
# aligning_dna()
#
# lengthening()
#
#protdnakorr_adaptation()
