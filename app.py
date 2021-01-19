from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    brand_dict = {
        "Maruti" : 20,
        "Hyundai" :	11,
        "Mahindra" : 19,
        "Tata" : 27,
        "Honda" : 10,
        "Toyota" : 28,
        "Ford" : 9,
        "Chevrolet" : 4,
        "Renault" :	25,
        "Volkswagen" : 29,
        "BMW" :	3,
        "Skoda" : 26,
        "Nissan" : 23,
        "Jaguar" : 13,
        "Volvo" : 30,
        "Datsun" : 6,
        "Mercedes-Benz" : 21,
        "Fiat" : 7,
        "Audi" : 2,
        "Lexus" : 17,
        "Jeep" : 14,
        "Mitsubishi" : 22,
        "Land" : 16,
        "Force" : 8,
        "Isuzu" : 12,
        "Kia" :	15,
        "Ambassador" : 0,
        "Daewoo" :	5,
        "MG" :	18,
        "Ashok" : 	24,
        "Opel" :	1


    }
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        seats = int(request.form['Seats'])
        mileage = int(request.form['Mileage'])
        engine = int(request.form['Engine'])
        max_power = int(request.form['MaxPower'])
        brand = brand_dict[request.form['Brand']]
        Owner=request.form['ownership']
        if(Owner == 'SecondOwner'):
            second_owner = 1
            third_owner = 0
            fourth_owner = 0
            test_drive = 0
        elif(Owner == 'ThirdOwner'):
            second_owner = 0
            third_owner = 1
            fourth_owner = 0
            test_drive = 0
        elif(Owner == 'FourthOwner'):
            second_owner = 0
            third_owner = 0
            fourth_owner = 1
            test_drive = 0
        elif(Owner == 'TestDriveCar'):
            second_owner = 0
            third_owner = 0
            fourth_owner = 0
            test_drive = 1
        else:
            second_owner = 0
            third_owner = 0
            fourth_owner = 0
            test_drive = 0
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
            Fuel_Type_LPG = 0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
            Fuel_Type_LPG = 0
        elif(Fuel_Type_Petrol=='LPG'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG = 1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG = 0
        Year=2021-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Trusmark_dealer = 0
        elif(Seller_Type_Individual == 'TrustmarkDealer'):
            Seller_Type_Individual=0
            Seller_Type_Trusmark_dealer = 1
        else:
            Seller_Type_Individual=0	
            Seller_Type_Trusmark_dealer = 0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Kms_Driven,seats,Year,mileage,engine,max_power,brand,
        Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Seller_Type_Individual,Seller_Type_Trusmark_dealer,
        Transmission_Mannual,fourth_owner,second_owner,test_drive,third_owner]])
        output=round(prediction[0],2)
        print(prediction)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
