# StockAnalysisWGmm
This project was built to test the plausubility of categorizing stock prices into oversold and overbought ranges using gaussian mixture models. A basic strategy to use with this model would be to buy a stock in the low oversold range and sell a stock in the high overbought range.


The SkLearn library was used for the gaussian mixture model with the RSI and MACD as the X training data. Labels are calculated from the same rsi and macd dataset used to train the model. 


To optimize the model a BIC value was calculated for models using 1 to 20 labels and 4 was choosen as the best number of labels. 
![num_groups_vs_bic](https://user-images.githubusercontent.com/82553480/143329705-68752574-dc43-47c0-b38a-2fecbce5658b.png)


The rsi and macd were also plotted with the label catergories highlighted in different colors. It was found that there is no 
clear boundaries for categorizing the data set. The chart also shows that there is a similar covarience between the macd and 
the rsi so 'tied' was used as the covarience type. Even though there are no clear boundries to caterorize the data the model
was able to seperate the data to be used for cateroizing stock trends.
![Indicator_Groups](https://user-images.githubusercontent.com/82553480/143328869-cc6eda1b-0459-4484-8fb6-1077e075218f.png)

Below is a video of the ui and how to run a test. The project come with and example data set "test_AAPL". To use live the access to the TD ameritrade api is required, just add you own API_KEY and ACCOUNT_NUMBER into the config file. After setting up the config file type any ticker into the input field in the ui it will pull in data for that ticker.  
https://user-images.githubusercontent.com/82553480/143331980-89988136-f6f2-4d0b-92e3-7a747cb73575.mp4








