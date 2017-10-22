
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split,KFold
from sklearn.ensemble import ExtraTreesClassifier,RandomForestClassifier,GradientBoostingClassifier
from sklearn.metrics import classification_report, log_loss
from sklearn.metrics import confusion_matrix

import random

random.seed(12345)

pd.options.display.max_columns = 100


# In[66]:

path = './'
name = ''
out_name = path + name + 'submission_py.csv'


# In[67]:


import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          doprint=True,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    if doprint:
        print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    if doprint:
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# In[68]:

# read data

train_data = pd.read_csv(path + name + 'train.csv')
test_data = pd.read_csv(path + name + 'test.csv')


# In[69]:

print(train_data.shape)
print(test_data.shape)


# In[70]:

# get first 5 seconds
qq = list(range(1,71))
X = train_data.iloc[:,qq].as_matrix()
Xt = test_data.iloc[:,qq].as_matrix()
y = train_data.iloc[:,-1].as_matrix()

print(X.shape)
print(Xt.shape)
print(y.shape)


# # Test XGBoost on first 5 seconds

# In[71]:

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.05)
print(X_train.shape)
print(X_val.shape)


# In[72]:

get_ipython().run_cell_magic(u'time', u'', u"from xgboost import XGBClassifier\ngbc = XGBClassifier(objective='multi:softprob',\n                    learning_rate=0.2,\n                    subsample=0.7,\n                    colsample_bytree=0.9,\n                    colsample_bylevel=0.7,\n                    max_depth=5,\n                    nthread=4,\n                    n_estimators=50,\n                    seed=1234)\n\ngbc.fit(X_train,y_train)\npred = gbc.predict(X_val)\nprint(classification_report(y_pred=pred,y_true=y_val))\npred_proba = gbc.predict_proba(X_val)\nprint('log_loss: {}'.format(log_loss(y_pred=pred_proba,y_true=y_val)))")


# In[73]:

cnf_matrix = confusion_matrix(y_val, pred)
plt.figure()
classes = range(0,25)
plot_confusion_matrix(cnf_matrix, classes, normalize=True, doprint=False, title='Normalized confusion matrix')


# In[74]:

#submit result

pred = gbc.predict(Xt)
pred = pred.astype(int)
df = pd.DataFrame(pred)
df.to_csv(out_name, header=False)


#compress result file
import gzip

in_data = open(out_name, "rb").read()
out_gz = out_name+".gz"
gzf = gzip.open(out_gz, "wb")
gzf.write(in_data)
gzf.close()



