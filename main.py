import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
import pickle
print("*LOADING AND READING DATA")
df=pd.read_csv("student-por.csv")
print(df)
df=df.drop(["Pstatus","Medu","Fedu","romantic","famsize"],axis=1)
print("REMOVING UNWANTED COLUMNS")
print(df)
print("*LABEL ENCODING")
encoders={}
categorical_columns=[
    "school","sex","Mjob","Fjob",
    "reason","guardian","address","schoolsup","famsup","paid","activities",
    "nursery","higher","internet"]
for col in categorical_columns:
    le=LabelEncoder()
    df[col]=le.fit_transform(df[col])
    encoders[col]=le
print(df)
print("*TRAINING AND TESTING DATA SPLITTING")
x=df.drop("G3",axis=1)
y=df["G3"]
x_train,x_test,y_train,y_test=train_test_split(x,y,
                                               test_size=0.2,
                                               random_state=42)
print("Trainig data:",x_train.shape)
print("Testing data:",x_test.shape)
print("Training labels:",y_train.shape)
print("Testing Labels",y_test.shape)

print("*RANDOM FOREST")
rf=RandomForestRegressor(random_state=42)
param_dist={
    'n_estimators':[100,200,300,500],
    'max_depth':[10,15,20,None],
    'min_samples_split':[2,5,10],
    'min_samples_leaf':[1,2,4],
    'max_features':['sqrt','log2',None]
    }
random_search=RandomizedSearchCV(estimator=rf,
                                 param_distributions=param_dist,
                                 n_iter=20,
                                 cv=5,
                                 scoring='r2',
                                 random_state=42,
                                 n_jobs=-1)
random_search.fit(x_train,y_train)
best_model=random_search.best_estimator_

rf_pred=best_model.predict(x_test)
rf_r2=r2_score(y_test,rf_pred)
with open("random_forest.pkl","wb") as file:
    pickle.dump(best_model,file)
print("Random Forest model saved as random_forest.pkl")
with open("label_encoders.pkl","wb") as file:
    pickle.dump(encoders,file)
print("Label encoders saved.")
print("Best Parameters:",random_search.best_params_)
print("R2 Score",rf_r2)


importance = pd.DataFrame({
    "Feature": x.columns,
    "Importance": best_model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance")
print(importance)

print("*SUPPORT VECTOR REGRESSION")
model=SVR()
model.fit(x_train,y_train)
svr_pred=model.predict(x_test)
svr_r2=r2_score(y_test,svr_pred)
print("R2 score:",svr_r2)

print("*Gradient Boost Regresoor")
model=GradientBoostingRegressor()
model.fit(x_train,y_train)
gbr_pred=model.predict(x_test)
gbr_r2=r2_score(y_test,gbr_pred)
print("R2 score:",gbr_r2)

print("*XG BOOST REGRESSOR")
xgb = XGBRegressor(
    objective='reg:squarederror',
    random_state=42
    )
param_dist = {
    'n_estimators': [100, 200, 300, 500],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'max_depth': [3, 4, 5, 6, 8],
    'subsample': [0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
    }
random_search = RandomizedSearchCV(
    estimator=xgb,
    param_distributions=param_dist,
    n_iter=20,
    cv=5,
    scoring='r2',
    random_state=42,
    n_jobs=-1
    )
random_search.fit(x_train, y_train)
best_xgb = random_search.best_estimator_
xgb_pred = best_xgb.predict(x_test)
xgb_r2 = r2_score(y_test, xgb_pred)
print("Best Parameters:", random_search.best_params_)
print("R2 Score:", xgb_r2)

with open("random_forest.pkl","rb") as file:
    model=pickle.load(file)
with open("label_encoders.pkl","rb") as file:
    encoders=pickle.load(file)
    
print("\nEnter Student Details")
def get_encoded_input(column,prompt):
    while True:
        value=input(prompt).strip().lower()
        classes=[c.lower() for c in encoders[column].classes_]
        if value in classes:
            index=classes.index(value)
            return encoders[column].transform([encoders[column].classes_[index]])[0]
        print("Invalid input!")
        print("Valid options:", ", ".join(encoders[column].classes_))
school=get_encoded_input("school","School (GP/MS): ")
sex=get_encoded_input("sex","Sex (M/F): ")
age=int(input("Age: "))
address=get_encoded_input("address","Address (U/R): ")
print("\nMother Job Options:")
print("teacher, health, services, at_home, other")
Mjob=get_encoded_input("Mjob","Mother Job: ")
print("\nFather Job Options:")
print("teacher, health, services, at_home, other")
Fjob=get_encoded_input("Fjob","Father Job: ")
print("\nReason Options:")
print("course, home, reputation, other")
reason=get_encoded_input("reason","Reason: ")
print("\nGuardian Options:")
print("mother, father, other")
guardian=get_encoded_input("guardian","Guardian: ")
traveltime=int(input("Travel Time: "))
studytime=int(input("Study Time: "))
failures=int(input("Failures: "))
schoolsup=get_encoded_input("schoolsup","School Support (yes/no): ")
famsup=get_encoded_input("famsup","Family Support (yes/no): ")
paid=get_encoded_input("paid","Paid Classes (yes/no): ")
activities=get_encoded_input("activities","Activities (yes/no): ")
nursery=get_encoded_input("nursery","Nursery (yes/no): ")
higher=get_encoded_input("higher","Higher Education (yes/no): ")
internet=get_encoded_input("internet","Internet (yes/no): ")
famrel=int(input("Family Relationship: "))
freetime=int(input("Free Time: "))
goout=int(input("Go Out: "))
Dalc=int(input("Weekday Alcohol: "))
Walc=int(input("Weekend Alcohol: "))
health=int(input("Health: "))
absences=int(input("Absences: "))
G1=int(input("G1 Marks: "))
G2=int(input("G2 Marks: "))
student=[[
    school,sex,age,address,Mjob,Fjob,reason,guardian,
    traveltime,studytime,failures,schoolsup,famsup,paid,
    activities,nursery,higher,internet,famrel,freetime,
    goout,Dalc,Walc,health,absences,G1,G2]]
student_df=pd.DataFrame(student,columns=x.columns)
prediction=model.predict(student_df)
print("Predicted G3:",prediction[0])