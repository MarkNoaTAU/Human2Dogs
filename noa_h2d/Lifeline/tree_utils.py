import numpy as np
import pandas as pd

import scipy
import dendropy
import re 
import os

from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram



def load_gtdb_tree():
    taxonomic_tree_path = './data/bac120_r207.tree'
    gtdb_tree = dendropy.Tree.get(path=taxonomic_tree_path, schema="newick")
    return gtdb_tree


def load_gtdb_taxonomic_info():
    taxaonomic_info_path = './data/bac120_metadata_r207/bac120_metadata_r207.tsv'
    taxaonomic_info = pd.read_csv(taxaonomic_info_path, sep='\t')
    taxaonomic_info['species'] = taxaonomic_info['gtdb_taxonomy'].str.extract('.*;s__(.*)')
    taxaonomic_info['accession'] = taxaonomic_info['accession'].apply(lambda x: x.replace('_', ' '))
    return taxaonomic_info


def load_gtdb_lifeline_subtree(lifeline_taxonomic_labels):
    """
        Retrain the subtree containing the Lifeline taxonomic information from GTDB tree.
        
        lifeline_taxonomic_labels: columns Taxonomy (species labels)
    """
    if os.path.exists("./data/lifeline_gtdb_v207_subtree.tree"):
        lifeline_gtdb_tree = dendropy.Tree.get(path="./data/lifeline_gtdb_v207_subtree.tree", schema="newick")
        taxaonomic_info = load_gtdb_taxonomic_info()
        taxaonomic_info_filtered = taxaonomic_info[taxaonomic_info['species'].isin(lifeline_taxonomic_labels)]
    else:
        lifeline_gtdb_tree = load_gtdb_tree()
        taxaonomic_info = load_gtdb_taxonomic_info()
        taxaonomic_info_filtered = taxaonomic_info[taxaonomic_info['species'].isin(lifeline_taxonomic_labels)]
        taxa_to_retain = set([taxon for taxon in gtdb_tree.taxon_namespace if taxon.label in list(taxaonomic_info_filtered.accession)])
        lifeline_gtdb_tree = gtdb_tree.extract_tree_with_taxa(taxa=taxa_to_retain)
        lifeline_gtdb_tree.write(path="./data/lifeline_gtdb_v207_subtree.tree", schema="newick")
    
    return lifeline_gtdb_tree, taxaonomic_info_filtered.set_index('accession')['species']


def get_species_phylogentic_distance_lifeline(lifeline_taxonomic_labels):
    lifeline_gtdb_tree, accession_to_species = load_gtdb_lifeline_subtree(lifeline_taxonomic_labels)
    
    # Get the phylogenetic distance (species to species):
    lifeline_phylogenetic_distance_matrix = lifeline_gtdb_tree.phylogenetic_distance_matrix()

    lifeline_phylogenetic_distance_matrix_data_table = lifeline_phylogenetic_distance_matrix.as_data_table()
    lifeline_phylogenetic_distance_matrix_df = pd.DataFrame(lifeline_phylogenetic_distance_matrix_data_table._data)
    lifeline_phylogenetic_distance_matrix_df = lifeline_phylogenetic_distance_matrix_df.rename(index=accession_to_species, columns=accession_to_species)

    return lifeline_phylogenetic_distance_matrix_df


def get_dendogram_representation_of_phylogentic_clustering(taxa_df):
    """
        Return dendogram, scipy heirarical clustering representation, according to the phylogentic distance. 
    """
    lifeline_phylogenetic_distance_matrix_df = get_species_phylogentic_distance_lifeline(lifeline_taxonomic_labels=taxa_df.columns)
    
    condensed_dist_matrix = squareform(lifeline_phylogenetic_distance_matrix_df)

    # Generate the linkage matrix from the condensed distance matrix
    
    Z = linkage(condensed_dist_matrix, method='average')
    
    dendro =  dendrogram(Z, labels=lifeline_phylogenetic_distance_matrix_df.index,  orientation='top')
    return dendro, Z