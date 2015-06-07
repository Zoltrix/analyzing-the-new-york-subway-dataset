import numpy as np
import pandas
import scipy
import statsmodels.api as sm
import matplotlib.pyplot as plt


"""
In this optional exercise, you should complete the function called
predictions(turnstile_weather). This function takes in our pandas
turnstile weather dataframe, and returns a set of predicted ridership values,
based on the other information in the dataframe.

In exercise 3.5 we used Gradient Descent in order to compute the coefficients
theta used for the ridership prediction. Here you should attempt to implement
another way of computing the coeffcients theta. You may also try using a reference implementation such as:
http://statsmodels.sourceforge.net/devel/generated/statsmodels.regression.linear_model.OLS.html

One of the advantages of the statsmodels implementation is that it gives you
easy access to the values of the coefficients theta. This can help you infer relationships
between variables in the dataset.

You may also experiment with polynomial terms as part of the input variables.

The following links might be useful:
http://en.wikipedia.org/wiki/Ordinary_least_squares
http://en.wikipedia.org/w/index.php?title=Linear_least_squares_(mathematics)
http://en.wikipedia.org/wiki/Polynomial_regression

This is your playground. Go wild!

How does your choice of linear regression compare to linear regression
with gradient descent computed in Exercise 3.5?

You can look at the information contained in the turnstile_weather dataframe below:
https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

Note: due to the memory and CPU limitation of our amazon EC2 instance, we will
give you a random subset (~10%) of the data contained in turnstile_data_master_with_weather.csv

If you receive a "server has encountered an error" message, that means you are hitting
the 30 second limit that's placed on running your program. See if you can optimize your code so it
runs faster.
"""


def predictions(weather_turnstile):
    # select out features
    features = weather_turnstile[['Hour', 'meanpressurei', 'meantempi', 'meanwindspdi', 'rain']]

    # add the UNIT feature with dummy variables
    dummy_units = pandas.get_dummies(weather_turnstile['UNIT'], prefix='unit')
    features = features.join(dummy_units)

    #we want to predict the hourly entries (this is our Y)
    values = weather_turnstile['ENTRIESn_hourly']

    #add a constant term (the intercept)
    features = sm.add_constant(features)

    #convert to arrays
    features = np.array(features)
    values = np.array(values)

    #train our ordinary least squares model
    model = sm.OLS(values, features)
    model = model.fit()

    #plot the distribution of normalized residuals
    plt.figure()
    plt.hist(model.norm_resid(), bins=50)
    plt.ylabel('Count')
    plt.xlabel('Normalized residuals')

    #predict
    prediction = model.predict(features)

    #normal probability plot
    residuals = model.resid  # residuals
    qq_plot = sm.qqplot(residuals, line='45', fit=True)

    #scatter plot of residuals
    plt.figure()
    plt.plot(prediction, residuals, '.')
    plt.plot([-2000, 14000], [0, 0], '-')
    plt.ylabel('Residuals')
    plt.xlabel('Predictions')
    plt.title('Predictions vs Residuals')

    return prediction, plt, qq_plot


weather_turnstile = pandas.read_csv('turnstile_data_master_with_weather.csv')
_, plt, qq_plot = predictions(weather_turnstile)

plt.show()
qq_plot