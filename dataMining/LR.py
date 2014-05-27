__author__ = 'davidoregan'


# Import my libarys
import pandas as pd
import pandas.io.sql as psql
import json
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from yhat import BaseModel
import MySQLdb
import numpy as np




# --------------------------------------------------------------------------------------------------------

# connect to my DB to get data, place data into a pandas Dataframe
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",port=8889,
db="carzone")

sql = """
        select *
            from vw_golf
      """
df = psql.frame_query(sql, db)
db.close()

# --------------------------------------------------------------------------------------------------------

# Read my test file, 10 lines
testing = pd.read_csv('wv_golf.csv')


# Edit Strings to narrow down my possible categories
#To Do!



# Do some basic file editing to make my data work with algorithm
# -------------------Training Set Management(From DB)------------------------------------------------

df['mileage'] = df['mileage'].str.replace('M', '')
df['mileage'] = df['mileage'].str.replace(',', '')
df['mileage'] = df['mileage'].astype('float')

age = 2014 - df['carYear']
df['carYear'] = age


df['price'] = df['price'].str.replace(',', '')
df['price'] = df['price'].str.replace('POA', '0')
df['price'] = df['price'].astype('float64')


# --------------------Test Set Management--------------------------------------------------------


testing['mileage'] = testing['mileage'].str.replace('M', '')
testing['mileage'] = testing['mileage'].str.replace(',', '')
testing['mileage'] = testing['mileage'].astype('float64')

age = 2014 - testing['carYear']
testing['carYear'] = age


# askingPrice = testing['price']
# my_dict = dict(askingPrice)



testing['price'] = testing['price'].str.replace(',', '')
testing['price'] = testing['price'].str.replace('POA', '0')
testing['price'] = testing['price'].astype('float64')






# --------------------------------------------------------------------------------------------------------


# Fill in any empy spaces as 0
df.fillna(0, inplace=True)
testing.fillna(0, inplace=True)


# --------------------------------------------------------------------------------------------------------

# Edit our dataframe to drop colums we dont need and seerate the price colum already there

df_no_price = df.drop(['price'], 1)
df_no_priceLink = df_no_price.drop(['link'], 1)
df_no_priceLinkTitle = df.drop(['ID','price', 'link', 'title'], 1)

# --------------------------------------------------------------------------------------------------------


# Do the same for our testing file
testing_no_priceLinkTitle = testing.drop(['price', 'link', 'title'], 1)

# --------------------------------------------------------------------------------------------------------


#Now use the sklearn DictVectorizor libary to map each colum from the data frame into a numpy array
# Transforms lists of feature-value mappings to vectors.
dv = DictVectorizer()
dv.fit(df_no_priceLinkTitle.T.to_dict().values())


# --------------------------------------------------------------------------------------------------------

# Create linear regression object
LR = LinearRegression()

# Train the model using the training sets(DataFrame without title, link or price and then price by itself)
LR.fit(dv.transform(df_no_priceLinkTitle.T.to_dict().values()), df.price)

# Explained variance score: 1 is perfect prediction
print ('Variance score: %.2f' % LR.score(dv.transform(df_no_priceLinkTitle.T.to_dict().values()), df.price))

# --------------------------------------------------------------------------------------------------------

# Predict function that uses yhat's basemodel
# This function allows me to use the transform method
#  This will map my input to the numpy array needed by the LR model
#  The predict function will then evaluate my LR model based on the numpy array



class predictFunction(BaseModel):

    #Place transformed data into numpy array for use
    def transform(self, doc):
        return self.dv.transform(doc)



    # x is our input vector(car information)
    #Predicted price is what our model determines based on the LR
    def predict(self, x):
        doc = self.dv.inverse_transform(x)[0]
        predicted = self.lr.predict(x)[0]
        return {'predictedPrice': predicted,
                'x': doc,
                # 'VS Asking Price:': AP
        }

# --------------------------------------------------------------------------------------------------------

# Start by passing our variables(transformed data frame and LR model to function above)
# Open a json file for output
# Display the predicted price as well as our car variables from our LR model earlier
# Store info in json file


predictedPrice = predictFunction(dv=dv, lr=LR)
print " "
with open('vw_golfDealz.txt', 'w') as outfile:
    for i in range(1580):
        outputPrice = predictedPrice.predict(predictedPrice.transform(testing.T.to_dict()[i]))
        print outputPrice
        json.dump(outputPrice, outfile)
        outfile.write('\n')

# --------------------------------------------------------------------------------------------------------







# References:
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.DictVectorizer.html
# http://en.wikipedia.org/wiki/Regression_analysis
# http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
# http://scikit-learn.org/0.11/auto_examples/linear_model/plot_ols.html
# http://stackoverflow.com/questions/15181311/using-dictvectorizer-with-sklearn-decisiontreeclassifier
# http://www.stephenbalaban.com/elegant-pythonic-solution-typeerror-json-serializable/




