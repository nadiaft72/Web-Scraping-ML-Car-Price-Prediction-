import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

file_name = "cars_data.csv"

car_data = pd.read_csv(file_name)

# Collect new car data from the user or use the default data (Acura, SH-AWD, 1046, 2, CA, 2019, 0).
default_data = input("We considered the following data: Acura,SH-AWD,1046,2,CA,2019,0. If you want to add another data enter 'y', else enter 'n': ")
if default_data.lower() == "y":
    default_data = input("Please enter the current model_name, model, mile, accident, location, year, price: ")

    # Encode categorical columns using LabelEncoder.
    categorical_columns = ["model_name", "model", "accident", "location", "year"]
    label_encoders = {}
    for column in categorical_columns:
        label_encoders[column] = LabelEncoder()
        car_data[column] = label_encoders[column].fit_transform(car_data[column])

    features = car_data.iloc[:, :-1]
    target = car_data.iloc[:, -1]

    # Train the DecisionTreeClassifier on the dataset.
    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(features, target)

    # Encode the default_data and predict its price.
    default_data_encoded = [int(label_encoders[column].transform([value])) for column, value in zip(categorical_columns, default_data.split(','))]
    new_price = classifier.predict([default_data_encoded[:-1]])[0]
    
    print("Predicted price for this car is:", new_price)
else:
    print("No additional data provided for prediction.")
