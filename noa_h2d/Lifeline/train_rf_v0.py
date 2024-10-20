import pandas as pd
import re
import time
import os

from joblib import Parallel, delayed
from multiprocessing import cpu_count

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold



def train_predict_blood_metabolites(m_name, taxonomy_deep, blood_metabolites, random_state):
    if os.path.exists(f'results/blood_metabolites/kfold_pred_v0_default_rf_{m_name}.pkl'):
        return
    X = taxonomy_deep
    y = blood_metabolites[m_name]

    X, y = X.align(y.dropna(), join = 'inner', axis=0)

    kfold_cv = KFold(n_splits=10)
    cv_pred = []

    for train_index, test_index in kfold_cv.split(X=X, y=y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        reg = RandomForestRegressor(random_state=random_state)
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        cv_pred.append(pd.Series(y_pred, index=X_test.index))


    cv_pred = pd.concat(cv_pred)
    cv_pred.name = m_name
    cv_pred.to_pickle(f'results/blood_metabolites/kfold_pred_v0_default_rf_{m_name}.pkl')



taxonomy_deep = pd.read_pickle('preprocessed_data/rarefied_kraken_species_level_taxonomy_filtered_ra.pkl')

blood_metabolites = pd.read_pickle('preprocessed_data/blood_metabolites_preprocessed.pkl')

random_state = 40

cpu_available = cpu_count()

start = time.time()

Parallel(n_jobs=cpu_available)(delayed(train_predict_blood_metabolites)(m_name, taxonomy_deep, blood_metabolites, random_state) for m_name in blood_metabolites.columns)

end = time.time()
print('{:.4f} s'.format(end-start))



