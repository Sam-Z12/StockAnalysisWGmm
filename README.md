# StockAnalysisWGmm
This project was built to test categorizing stock prices into oversold and overbought ranges using gaussian mixture models. A basic strategy to use with this model would be to buy a stock in the low oversold range and sell a stock in the high overbought range.

The SkLearn library was used for the gaussian mixture model with the RSI and MACD as the X training data. Labels are calculated from the same X training data set. 

To optimize the model a BIC value was calculated for models using 1 to 20 labels and 4 was choosen as the best number of labels. 
The rsi and macd were also plotted with the label catergories highlighted in different colors. It was found that there is no 
clear boundaries to categories the data set from. The chart also show that there is a similar covarience betweem the macd and 
the rsi so 'tied' was used as the covarience type. 

The results of the two optimization tests are plotted below.  
![num_groups_vs_bic](https://user-images.githubusercontent.com/82553480/143329705-68752574-dc43-47c0-b38a-2fecbce5658b.png)
![Indicator_Groups](https://user-images.githubusercontent.com/82553480/143328869-cc6eda1b-0459-4484-8fb6-1077e075218f.png)




https://user-images.githubusercontent.com/82553480/143331980-89988136-f6f2-4d0b-92e3-7a747cb73575.mp4








