""" lifeline deep target loaders """

import numpy as np
import pandas as pd

import data_loaders



def load_triglyceride(blood=None):
    if blood is None:
        blood = data_loaders.load_blood_measurements()
    trig = blood['triglyceride_result_all_m_1'].groupby(blood.index).max()
    trig.name = 'triglyceride'
    return trig


def load_triglyceride_at_risk():
    trig = load_triglyceride()
    return trig >= 1.7

def load_hdl(blood=None):
    if blood is None:
        blood = data_loaders.load_blood_measurements()
    hdl = blood['hdlchol_result_all_m_1'].groupby(blood.index).max()
    hdl.name = 'hdl'
    return hdl

def load_hdl_at_risk(blood=None):
    hdl = load_hdl(blood=blood)
    age_gender = data_loaders.load_age_and_gender_data()
    hdl_risk = pd.concat([hdl.to_frame('hdl'), age_gender['gender']], axis=1)
    def define_risk(data):
        if data.gender == 'FEMALE':
            return data.hdl < 1.3 
        elif data.gender == 'MALE':
            return data.hdl < 1.0
        else:
            raise ValueError("Gender must be FEMALE or MALE (non PC im sorry :(" )
    return hdl_risk.apply(define_risk, axis=1)
