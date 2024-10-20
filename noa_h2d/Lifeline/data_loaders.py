""" lifeline deep data loaders """

import numpy as np
import pandas as pd
import os

def load_age_and_gender_data():
    deep_link = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/OV22_00666_deep_linkage_file-v2.csv")
    a1v2 = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/1a_v_2_results_filtered_to_deep.csv")
    age_gender = pd.merge(a1v2[['age','gender','project_pseudo_id']], deep_link,  on = "project_pseudo_id",how='inner').set_index('LLDEEP_ID')[['age','gender']]
    age_gender = age_gender.groupby(age_gender.index).first()
    return age_gender


def load_blood_measurements():
    deep_link = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/OV22_00666_deep_linkage_file-v2.csv")
    a1v2 = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/1a_v_2_results_filtered_to_deep.csv")
    vo = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/variable_overview.csv")
    blood_vo = vo[(vo["subsection"] == "Biospecimen: Blood") & (vo["1a_v_2"] == "x")]["variable_name"].values
    a1v2 = pd.merge(a1v2, deep_link,  on = "project_pseudo_id",how='inner')
    blood = a1v2.set_index('LLDEEP_ID')[blood_vo]
    blood = blood.replace(to_replace={'$5':'nan'}).astype(float)
    return blood


def load_bmi_data():
    deep_link = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/OV22_00666_deep_linkage_file-v2.csv")
    a1v1 = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/1a_v_1_results_filtered_to_deep.csv")
    # deep_link = pd.read_csv(“metadata/OV22_00666_deep_linkage_file-v2.csv”)
    a1v1_link = pd.merge(a1v1, deep_link, how="inner", on="project_pseudo_id")
    bmi_data = a1v1_link.set_index('LLDEEP_ID')[['bodylength_cm_all_m_1','bodyweight_kg_all_m_1']]
    bmi_data = bmi_data.groupby(bmi_data.index).median()
    #  BMI = weight (kg) ÷ height2 (meters)
    bmi_data['bmi'] = bmi_data['bodyweight_kg_all_m_1'] / ((bmi_data['bodylength_cm_all_m_1'] / 100) ** 2)
    bmi_data['bmi_score'] = np.where(
            (bmi_data['bmi'] >= 18.5) & (bmi_data['bmi'] <= 25),0,
            np.where((bmi_data['bmi'] > 25) & (bmi_data['bmi'] <= 30),0.5,
                np.where(bmi_data['bmi'] < 18.5,1,1)))
    return bmi_data

def load_taxa_in_relative_abundance(from_file=True, PERCENTAGE_OF_SAMPLES=10, RA_THRESHOLD=0.001):
    if from_file:
        return pd.read_pickle('preprocessed_data/rarefied_kraken_species_level_taxonomy_filtered_ra.pkl')
    else:
        taxonomy_deep = pd.read_pickle('preprocessed_data/rarefied_kraken_species_level_taxonomy.pkl')
        archea_species = ['Methanobrevibacter_A smithii', 'Methanobrevibacter_A smithii_A']
        taxonomy_deep = taxonomy_deep.drop(columns=archea_species)
        simple_ra = taxonomy_deep.divide(taxonomy_deep.sum(axis=1), axis=0)
        min_number_of_samples = int((taxonomy_deep.shape[0] / 100) * PERCENTAGE_OF_SAMPLES)
        non_rare_columns = taxonomy_deep.columns[
            ((simple_ra >= RA_THRESHOLD).sum(axis=0)) >= min_number_of_samples]
        len(non_rare_columns)
        print(f"Species that at least {PERCENTAGE_OF_SAMPLES} % of the samples have relative abundance above the threshold: {RA_THRESHOLD}")
        print(f"{len(non_rare_columns)} out of {taxonomy_deep.shape[1]} species, aka {round((len(non_rare_columns) / taxonomy_deep.shape[1]) * 100, 2)}%")
        return simple_ra[non_rare_columns]

def load_taxa_in_read_count(PERCENTAGE_OF_SAMPLES=10, RA_THRESHOLD = 0.001):
    # Load rarefired read count 
    taxonomy_deep = pd.read_pickle('preprocessed_data/rarefied_kraken_species_level_taxonomy.pkl')
    archea_species = ['Methanobrevibacter_A smithii', 'Methanobrevibacter_A smithii_A']
    taxonomy_deep = taxonomy_deep.drop(columns=archea_species)
    
    # Filter Rare Taxa
    simple_ra = taxonomy_deep.divide(taxonomy_deep.sum(axis=1), axis=0)
    min_number_of_samples = int((taxonomy_deep.shape[0] / 100) * PERCENTAGE_OF_SAMPLES)
    non_rare_columns = taxonomy_deep.columns[
        ((simple_ra >= RA_THRESHOLD).sum(axis=0)) >= min_number_of_samples]
    len(non_rare_columns)
    print(f"Species that at least {PERCENTAGE_OF_SAMPLES} % of the samples have relative abundance above the threshold: {RA_THRESHOLD}")
    print(f"{len(non_rare_columns)} out of {taxonomy_deep.shape[1]} species, aka {round((len(non_rare_columns) / taxonomy_deep.shape[1]) * 100, 2)}%")
    # Return read count
    return taxonomy_deep[non_rare_columns]
    

def load_medical_treatmeant_info(verbose=False):
    """ 
        Use DEEP questionnaire 1 to load medical treatmeant metadata. 
    """
    a1q1_variables = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/1a_q_1_variables.csv")
    a1q1_results = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/1a_q_1_results.csv")
    a1q1_enumerations = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/1a_q_1_enumerations.csv")
    
    deep_link = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/OV22_00666_deep_linkage_file-v2.csv")
    a1q1_results = pd.merge(a1q1_results, deep_link,  on = "project_pseudo_id",how='inner')
    
    vo = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/variable_overview.csv")
    medical_treatmeant_variables_names = vo[(vo['section'] == 'Medical treatment') & (vo['subsection'] == 'Medication')]['variable_name'].tolist()
    # Medical information contain in this metadata:
    if verbose:
        print('-------------------- Medical information contain in this metadata: -------------------- ')
        print('Variables (information) definition:')
        for var in medical_treatmeant_variables_names:
            print(f'{var}: {vo[vo["variable_name"] == var]["definition_en"].iloc[0]}')
        
        print('Variables representation in results:')
        print(a1q1_enumerations[a1q1_enumerations['variable_name'].isin(medical_treatmeant_variables_names)])
    
    medical_treatmeant_info = a1q1_results.set_index('LLDEEP_ID')[medical_treatmeant_variables_names]

    def process_results(x):
        if x == '$6':
            return None 
        if pd.isna(x):
            return None 
        return int(x)

    medical_treatmeant_info = medical_treatmeant_info.map(process_results)
    return medical_treatmeant_info
    
    
def got_hormonal_treatment_or_therapy(x):
    """
        Process medical_treatmeant_info (accept to get rows of load_medical_treatmeant_info result) and extract weather or not the patient recieved hormonal treatment 
    """
    got_hormonal_treatment = (x['hormonal_treatment_adu_q_1'] == 1) or (x['hormonal_treatment_adu_q_2'] == 1) or (x['hormonal_treatment_adu_q_3'] == 1)
    got_hormonal_therapy =  (x['hormone_therapy_adu_q_1'] == 1) or ( x['hormone_therapy_adu_q_1_b'] == 1)
    return got_hormonal_treatment or got_hormonal_therapy


def load_antibiotics_use_information():
    """  
        Extracting antibiotic usage information using the ATC code data from variable 1 a1. 
        
        "The Anatomical Therapeutic Chemical code: a unique code assigned to a medicine according to the organ or system it works on and how it works."

        The function return subject that took antibiotic according to ATC code. 
        
        Subject that took medicien with ATC code starting with J01, J02 or J04 - will be marked as subject how took antibiotic.

        See more information hear: 
        https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4136045/table/T1/
    """
    deep_link = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/OV22_00666_deep_linkage_file-v2.csv")    
    a1v1 = pd.read_csv("/groups/umcg-lifelines/tmp01/projects/ov22_0666/personal_directories/talbamberger/metadata/1a_v_1_results_filtered_to_deep.csv")
    a1v1_link = pd.merge(a1v1, deep_link, how="inner", on="project_pseudo_id")
    
    def atc_code_antibiotics(x):
        if pd.isna(x):
            return False
        return ('J01' in x) or ('J02' in x) or ('JO4' in x)

    medications_types = a1v1_link.set_index('LLDEEP_ID')[pd.Series(a1v1.columns).str.extract('(.*atc_code_adu_c_1_.*)').dropna().squeeze().to_list()]
    subject_take_antibiotics = medications_types.map(atc_code_antibiotics).any(axis=1).groupby(medications_types.index).any()
    return subject_take_antibiotics


def load_medication_per_subject_filter(account_for_laxatives=True):
    """
    Return indexes of subjects that took medication that alter the experiment result (multi-omic analysis, including microbiome specifcally). 
    More specifically, excludedparticipants who were taking antibiotic or other potential microbiome-modifying drugs or who were on lipid-lowering medication."
    
    This subject should be filter out.
    We will account for the following:
    * People how took medication for gastrointestinal complaints, digestives: 'otc_digestion_adu_q_1', in questionnaire 1
    * People how took medication for an overactive or underactive thyroid 'thyroid_medication_adu_q_1_a', in questionnaire 1
    * People how took laxatives 'otc_laxatives_adu_q_1' in questionnaire 1
    * People how took antibiotics (according to ATC code)
    
    """
    medical_treatmeant_info = load_medical_treatmeant_info()
    subject_take_antibiotics = load_antibiotics_use_information()
    if account_for_laxatives:
         return medical_treatmeant_info[(medical_treatmeant_info['otc_digestion_adu_q_1'] == 1) | (medical_treatmeant_info['thyroid_medication_adu_q_1_a'] == 1) | (medical_treatmeant_info['thyroid_medication_adu_q_1_b'] == 1) | (medical_treatmeant_info['otc_laxatives_adu_q_1'] == 1) ].index.union(subject_take_antibiotics[subject_take_antibiotics].index)
    else: 
        return medical_treatmeant_info[(medical_treatmeant_info['otc_digestion_adu_q_1'] == 1) | (medical_treatmeant_info['thyroid_medication_adu_q_1_a'] == 1) | (medical_treatmeant_info['thyroid_medication_adu_q_1_b'] == 1) ].index.union(subject_take_antibiotics[subject_take_antibiotics].index)
    

    
    