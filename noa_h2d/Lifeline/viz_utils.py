import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def vis_continous_pred(pred, y):
    """ scatter and hist plots of prediction and target for continus variables """
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    sns.histplot(pred, ax=axes[0], label='Predictions', color='blue', kde=False, bins=30, stat='density')
    sns.histplot(y, ax=axes[0], label='Targets', color='orange', kde=False, bins=30, stat='density')

    axes[0].set_title(f'{m_name}')
    axes[0].set_xlabel(f'{m_name} Value')
    axes[0].set_ylabel('Density')
    axes[0].legend()

    min_v, max_v = min(pred.min(), y.min()), max(pred.max(), y.max())

    axes[1].set_xlim((min_v, max_v))
    axes[1].set_ylim((min_v, max_v))

    axes[1].scatter(x=y, y=pred)
    axes[1].plot([min_v, max_v], [min_v, max_v], linestyle='--', color='red')


    axes[1].set_title(m_name)
    axes[1].set_xlabel(f'Target')

    plt.tight_layout()
    plt.show()

