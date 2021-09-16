import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import KFold

def _LinearRegression(A, b):
    reg = linear_model.LinearRegression().fit(A, b)
    return reg.coef_, reg.intercept_

def _CrossValidation(A, b, kfold):
    kf = KFold(n_splits = kfold)
    error_list = []

    for train_index, test_index in kf.split(A):
        A_train, A_test = A[train_index], A[test_index]
        b_train, b_test = b[train_index], b[test_index]
        _coef, _bias = _LinearRegression(A_train, b_train)
        error_list.append(np.mean(np.absolute(b_test - (np.dot(A_test, _coef) + _bias))))
        
    return np.mean(error_list)

def bestAttribute(A, b):
    error_list = []
    
    for i in range(A.shape[1]):
        cv_process = _CrossValidation(A[:, i].reshape(-1, 1), b, 15)
        error_list.append(cv_process)
        
    return error_list, np.argmin(error_list)

def Model_Builder(A, b, error_list, labels):
    labelCount = len(labels)
    sortedError = np.argsort(error_list)
    allAttrError = _CrossValidation(A, b, 15)
    
    error_list = [] 
    cvErrorList = []
    attrList = []
    
    for i in range(2, labelCount - 1):
        pickedAttr = sortedError[:i]
        A_proceed = A[:, pickedAttr]
        pickedAttrError = _CrossValidation(A_proceed, b, 15)
        cvErrorList.append(pickedAttrError)
        error_list.append(np.absolute(allAttrError - pickedAttrError))
        attrList.append(pickedAttr)
    
    return cvErrorList, attrList, np.argmin(error_list)
        
def main():
    dataset = pd.read_csv('wine.csv', sep=';')
    
    labels = dataset.columns
    attributes = np.array(dataset.iloc[:, : -1])
    quality = np.array(dataset.iloc[:, -1])

    _coef, _bias = _LinearRegression(attributes, quality)
    print(f'Model: y = {_bias} + {_coef}*x')
    print('-----------------------------------------------')
    
    error_list, best_one = bestAttribute(attributes, quality)
    _bestone_coef, _bestone_bias = _LinearRegression(attributes[:, best_one].reshape(-1, 1), quality)
    print(f'Best attribute is {labels[best_one]}')
    print(f'Attribute model: y = {_bestone_bias} + {_bestone_coef}*x')
    print(f'Attribute error: {error_list[best_one]}')
    
    for i in range(len(error_list)):
        spaces = 25 - len(labels[i])
        print(labels[i], ' ' * spaces, error_list[i])
    print('-----------------------------------------------')
    
    cvErrorList, attrList, myBest = Model_Builder(attributes, quality, error_list, labels)
    _myBest_coef, _myBest_bias = _LinearRegression(attributes[:,attrList[myBest]], quality)
    print(f'Best attributes are {list(labels[attrList[myBest]])}')
    print(f'Attributes model: y = {_myBest_bias} + {_myBest_coef}*x')
    print(f'Attributes error: {cvErrorList[myBest]}')
    for i in range(len(attrList)):
        print(attrList[i], ' ' * (25 - i * 3), cvErrorList[i])
 
if __name__ == '__main__':
    main()