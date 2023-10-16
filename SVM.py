from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from util import get_data
import time

if __name__ == '__main__':
    #input parameter C, gamma, and deciding the kernal type
    param_grid={'C':[0.1,1,10,100],'gamma':[0.0001,0.001,0.1,1],'kernel':['rbf']}
    svc=svm.SVC(probability=True)

    #tunes hyperparameters 
    model=GridSearchCV(svc,param_grid)

    x_train, y_train, x_test, y_test = get_data()

    startTime = time.perf_counter()

    #training model
    model.fit(x_train,y_train)

    endTime = time.perf_counter()

    modelTrainTime = endTime-startTime
    y_pred=model.predict(x_test)
    print("It took:", modelTrainTime/60, "minutes to train the model")
    print(f"The model is {accuracy_score(y_pred,y_test)*100}% accurate")