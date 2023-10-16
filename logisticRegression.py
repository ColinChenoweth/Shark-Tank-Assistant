import time
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from util import get_data


if __name__ == '__main__':
    
    x_train, y_train, x_test, y_test = get_data()
    print(' data loaded')

    print('training...')

    start_time = time.time()
    logReg = LogisticRegression()
    logReg = logReg.fit(x_train, y_train)
    y_pred = logReg.predict(x_test)

    print("Accuracy of Logistic Regression: ", accuracy_score(y_test, y_pred))
    print("Time for Logistic Regression: ", time.time() - start_time)
    