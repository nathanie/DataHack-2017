function readAndSubmit_sample2()

%% read data
train = readtable('train.csv');
test = readtable('test.csv');

X_train = table2array(train(:,2:71)); % take first 5 Sec from train data
Y_train = table2array(train(:,'class'));

%% Classify
ClassTreeEns = fitensemble(X_train,Y_train,'AdaBoostM2',10,'tree');

%% predict
X_test = table2array(test(:,2:71)); % take first 5 Sec from test data
Y_test_predict = predict(ClassTreeEns,X_test);

submission = [table2array(test(:,1)) Y_test_predict];
dlmwrite('submission_matlab.csv', submission, 'delimiter', ',', 'precision', 9); 
gzip('submission_matlab.csv');
end
