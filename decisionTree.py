
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from util import get_data

if __name__ == '__main__':
    
    x_train, y_train, x_test, y_test = get_data()
    print(' data loaded')


    print('training decision tree')

    start_time = time.time()
    clf = DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    print("Accuracy of Decision Tree: ", accuracy_score(y_test, y_pred))
    print("Time for Decision Tree: ", time.time() - start_time)


    #export_graphviz(clf, out_file='dtree.dot', filled=True, rounded=True, special_characters=True, class_names=categories)