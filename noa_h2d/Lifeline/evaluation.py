import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sklearn
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay
from shap import Explainer, summary_plot
from sklearn.metrics import PrecisionRecallDisplay


def plot_precision_recall_curve(clf, X_train, y_train, X_test, y_test):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    axes[0].plot(np.arange(0, 1.1, 0.1), np.arange(0, 1.1, 0.1), linestyle='--', color='red')
    axes[1].plot(np.arange(0, 1.1, 0.1), np.arange(0, 1.1, 0.1), linestyle='--', color='red')

    PrecisionRecallDisplay.from_estimator(clf, X_train, y_train, ax=axes[0])
    axes[0].set_title('train')

    PrecisionRecallDisplay.from_estimator(clf, X_test, y_test, ax=axes[1])
    axes[1].set_title('test')
    plt.show()


def plot_clf_roc(clf, X_train, y_train, X_test, y_test):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    axes[0].plot(np.arange(0, 1.1, 0.1), np.arange(0, 1.1, 0.1), linestyle='--', color='red')
    axes[1].plot(np.arange(0, 1.1, 0.1), np.arange(0, 1.1, 0.1), linestyle='--', color='red')

    RocCurveDisplay.from_estimator(clf, X_train, y_train, ax=axes[0])
    axes[0].set_title('train')

    RocCurveDisplay.from_estimator(clf, X_test, y_test, ax=axes[1])
    axes[1].set_title('test')
    plt.show()
    
    
def plot_shap_values(clf, X_train, y_train, X_test, y_test, summary_plot_kwargs):
    explainer = Explainer(clf)
    shap_values = explainer.shap_values(X_train)
    summary_plot(shap_values[:,:,0], X_train, show=False, **summary_plot_kwargs)
    plt.title('train')
    plt.show()

    shap_values = explainer.shap_values(X_test)
    summary_plot(shap_values[:,:,0], X_test, show=False, **summary_plot_kwargs)

    plt.title('test')
    plt.show()
    
    
def report_clf_preformance(clf, X_train, y_train, X_test, y_test):
    y_pred_test = clf.predict(X_test)
    y_pred_test = pd.Series(y_pred_test, index=X_test.index)
    print(classification_report(y_true=y_test , y_pred=y_pred_test))
    
    plot_clf_roc(clf, X_train, y_train, X_test, y_test)
    
    plot_precision_recall_curve(clf, X_train, y_train, X_test, y_test)
    
    ConfusionMatrixDisplay.from_estimator(clf, X_train, y_train)
    plt.show()
    
    ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test)
    plt.show()
    
    print("feature importance:")
    if type(clf) == sklearn.ensemble._forest.RandomForestClassifier:
        # Explain feature importance using SHAP values
        plot_shap_values(clf, X_train, y_train, X_test, y_test, summary_plot_kwargs=dict())
        plot_shap_values(clf, X_train, y_train, X_test, y_test, summary_plot_kwargs=dict(plot_type="bar"))
    elif type(clf) == sklearn.linear_model._logistic.LogisticRegression:
        # Explain feature importance using the coefficient values:
        pd.Series(clf.coef_[0], index=X_train.columns).plot.bar()
        plt.title('Feature coefficient')
        plt.show()
