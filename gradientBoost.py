import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import GradientBoostingClassifier
from util import get_data

if __name__ == '__main__':
    x_train, y_train, x_test, y_test = get_data()
    print('Data loaded')

    print('Training gradient boosting classifier')

    start_time = time.time()
    clf = GradientBoostingClassifier(random_state=42)
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    print("Accuracy of Gradient Boosting Classifier: ", accuracy_score(y_test, y_pred))
    print("Time for Gradient Boosting Classifier: ", time.time() - start_time)
