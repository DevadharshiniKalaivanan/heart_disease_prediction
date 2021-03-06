from flask import Flask,render_template,request
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle as pkl


app=Flask(__name__,static_url_path='/static')
model=pkl.load(open('heart_prediction.pkl','rb'))

@app.route('/')
def main():
    return render_template('first.html')

@app.route('/first')
def first():
    return render_template('first.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

sc=StandardScaler()
@app.route('/result',methods=['POST'])
def home():
    #cp_1=0
    cp_2=0
    cp_3=0
    restecg_1=0
    age=request.form['age']
    sex_1=request.form['gender']
    slope_1=0
    ca_2=0
    ca_3=0
    ca_4=0
    thal_2=0
    thal_3=0
    if(sex_1=='Female'):
        sex_1=0
    else:
        sex_1=1
    cp_1=request.form['cp']
    if(cp_1=='Atypical Angina'):
        cp_1=1
        cp_2=0
        cp_3=0
    elif(cp_1=='Non Angina'):
        cp_1=0
        cp_2=1
        cp_3=0
    else:
        cp_1=0
        cp_2=0
        cp_3=1
    rating_bp=request.form['trestbps']
    chol=request.form['chol']
    fbs_1=request.form['fbs']
    if(fbs_1=='yes'):
        fbs_1=1
    else:
        fbs_1=0
    restecg_2=request.form['restecg']
    if(restecg_2=='ST-T wave abnormality'):
        restecg_1=1
        restecg_2=0
    else:
        restecg_1=0
        restecg_2=1
    thalach=request.form['thalach']
    exang_1=request.form['exang']
    if(exang_1=='yes'):
        exang_1=1
    else:
        exang_1=0
    oldpeak=request.form['oldpeak']
    slope_2=request.form['slope']
    if(slope_2=='downsloping'):
        slope_2=1
        slope_1=0
    else:
        slope_1=1
        slope_2=0
    ca_1=request.form['ca']
    if(ca_1==1):
        ca_1=1
        ca_2=0
        ca_3=0
        ca_4=0
    elif(ca_1==2):
        ca_1=0
        ca_2=1
        ca_3=0
        ca_4=0
    elif(ca_1==3):
        ca_1=0
        ca_2=0
        ca_3=1
        ca_4=0
    else:
        ca_1=0
        ca_2=0
        ca_3=0
        ca_4=0
    thal_1=request.form['thal']
    if(thal_1=='Fixed Defect'):
        thal_1=1
        thal_2=0
        thal_3=0
    elif(thal_1=='Reversible defect'):
        thal_1=0
        thal_2=1
        thal_3=0
    else:
        thal_1=0
        thal_2=0
        thal_3=1
    numerical_data=(age,rating_bp,chol,thalach,oldpeak)
    numerical_data_numpy=np.asarray(numerical_data)
    numerical_data_reshape=numerical_data_numpy.reshape(1,-1)
    std_data=sc.fit_transform(numerical_data_reshape)

    categorical_data=(sex_1,cp_1,cp_2,cp_3,fbs_1,restecg_1,restecg_2,exang_1,slope_1,slope_2,ca_1,ca_2,ca_3,ca_4,thal_1,thal_2,thal_3)
    categorical_data_numpy=np.asarray(categorical_data)
    categorical_data_reshape=categorical_data_numpy.reshape(1,-1)

    output=np.hstack([std_data,categorical_data_reshape])
    predict=model.predict(output)
    prediction=round(predict[0],2)

    return render_template('result.html',data=prediction)
    
    

if __name__=='__main__':
    app.run(debug=True)



    
