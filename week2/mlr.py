#  source ~/test27/bin/activate

import graphlab
from math import log

sales = graphlab.SFrame('kc_house_data.gl/')

train_data,test_data = sales.random_split(.8,seed=0)

example_features = ['sqft_living', 'bedrooms', 'bathrooms']
example_model = graphlab.linear_regression.create(train_data, target = 'price', features = example_features,
                                                  validation_set = None)

example_weight_summary = example_model.get("coefficients")
print example_weight_summary

example_predictions = example_model.predict(train_data)
print example_predictions[0] # should be 271789.505878

def get_residual_sum_of_squares(model, data, outcome):
    # First get the predictions
    prediction = model.predict(data)
    # Then compute the residuals/errors
    residuals = prediction - outcome
    # Then square and add them up
    RSS = residuals*residuals
    RSS = RSS.sum()
    return(RSS)

rss_example_train = get_residual_sum_of_squares(example_model, test_data, test_data['price'])
print rss_example_train # should be 2.7376153833e+14

train_data['bedrooms_squared'] = train_data['bedrooms'].apply(lambda x: x**2)
test_data['bedrooms_squared'] = test_data['bedrooms'].apply(lambda x: x**2)

train_data['bed_bath_rooms'] = train_data['bedrooms']*train_data['bathrooms']
train_data['log_sqft_living'] = train_data['sqft_living'].apply(lambda x: log(x))
train_data['lat_plus_long'] = train_data['lat'] + train_data['long']

test_data['bed_bath_rooms'] = test_data['bedrooms']*test_data['bathrooms']
test_data['log_sqft_living'] = test_data['sqft_living'].apply(lambda x: log(x))
test_data['lat_plus_long'] = test_data['lat'] + test_data['long']

m1= test_data['bedrooms_squared'].mean()
m2= test_data['bed_bath_rooms'].mean()
m3= test_data['log_sqft_living'].mean()
m4= test_data['lat_plus_long'].mean()

print m1
print m2
print m3
print m4

model_1_features = ['sqft_living', 'bedrooms', 'bathrooms', 'lat', 'long']
model_2_features = model_1_features + ['bed_bath_rooms']
model_3_features = model_2_features + ['bedrooms_squared', 'log_sqft_living', 'lat_plus_long']

model1 = graphlab.linear_regression.create(train_data, target = 'price', features = model_1_features,
                                                  validation_set = None)
model2 = graphlab.linear_regression.create(train_data, target = 'price', features = model_2_features,
                                                  validation_set = None)
model3 = graphlab.linear_regression.create(train_data, target = 'price', features = model_3_features,
                                                  validation_set = None)

model1.coefficients
model2.coefficients
model3.coefficients

RSS1 = get_residual_sum_of_squares(model1, train_data, train_data['price'])
RSS2 = get_residual_sum_of_squares(model2, train_data, train_data['price'])
RSS3 = get_residual_sum_of_squares(model3, train_data, train_data['price'])
