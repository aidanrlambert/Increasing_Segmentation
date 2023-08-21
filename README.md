# Description of Project
Segments a range into a specified number of segments such that the size of each segment is equally larger than the previous.
For example, the range of 0-55 can be segmented into the series [1, 3, 6, 10, 15, 21, 28, 36, 45, 55] which has segment sizes of [2, 3, 4, 5, 6, 7, 8, 9, 10].
Each segment size (i.e. scale factor) is 1 larger than that of the previous segment.

# Using the long solve method
This method works by guess-and-check. 
An initial guess (1.0) is made for the scaling factor. From this guess, we produce a series where each segment size is [scaling factor] larger than the last.
If this guess produces a series whose last value is not equal to the maximum of the specified range, the scaling factor is adjusted and a new series generated.
The process is repeated until a series is found such that the last value of the series is equal to the maximum of the specified range.

This is done simply by:
```
from LongSolve import *
guess, maxes = solve(maximum_of_range, number_of_segments)
```

For example, given a range of 0-55 split into 10 segments: maximum_of_range = 55 and number_of_segments = 10 <br/>
Input:
```
solve(55, 10)
```
Output:
```
(1.0, [1.0, 3.0, 6.0, 10.0, 15.0, 21.0, 28.0, 36.0, 45.0, 55.0])
```
# Trying to find a faster method
## Analysis of Long Solve Method for 250,000 Unique Input Combinations

The long solve method is, as it's name might suggest, long. It involves a heavy use of guess-and-check requiring many iterations and computations. By looking at the scale factors produced for a multitude of different input values, we can attempt to derive the mathematical formula that would predict the scale factor for any given input. </br>

To do this, 250,000 test cases were generated using the Long Solve method. This involved 10,000 random range sizes from 100 - 1,000,000 paired with 25 different random choices for number of segments (possible values were 5 - 50).

Charting the scale factors generated vs the range size for these 250,000 cases shows a linear relationship between range size and scale factor. </br>
![Figure 1](Figures/Figure_1.png) </br>
Each different color in the above graph represents scale factor vs range size for only one choice of number of segments. From this, we can deduce that there must be some relationship between the number of segments and the slope of scale factor vs range size. </br>
![Figure_2](Figures/Figure_2.png) </br>

If you've spent some (a lot of) time looking at numbers, you might recognize that shape. It looks just a bit like $1 \over x^2$. If we take a look at the above graph overlayed with a chart of $1 \over x^2$, we can see they are very similar. </br>
![Figure_2b](Figures/Figure_2b.png) </br>


And if we plot the cross-section of our predictions and the actual value found by the Long Solve method, we see a straight line </br>
![Figure_3](Figures/Figure_3.png) </br>

with a slope of (1.72 $\pm$ 0.01). This tells us that the relationship between the number of segments and the scale\range slope is $(1.72 \pm 0.01) \over (number\ of\ segments)^2$. </br>
From here, we can subsitute the prediction for the slope of scale/range into the relationship of scale vs range, or $(1.72 \pm 0.01)\ \dot \ \ Range \over (number\ of\ segments)^2$. </br> </br>
This equation does yeild close results for predicting the actual value of the scale factor, but the predictions have an unsatisfying RMS error of 247 - too large to yeild accurate predictions. However, if we use this newfound equation for making the initial guess during the Long Solve method, we can reduce the time spent operating. Runtime can be further reduced by using the uncertainty in our predicition for setting the initial value by which we adjust our scale factor guess when it is above or below the true value, or $0.01\ \dot \ \ Range \over (number\ of\ segments)^2$, as it reduces the amount of time spent iterating over small intervals. </br> </br>

To find the effect on performance from using the equation, we adjust the function code from a simple
```
scale_guess = 1.0 # Current guess for the correct scale factor
scaler = 1.0 # Amount to adjust the scale factor guess by when last value of series is not equal to [final_max]
```
to
```
scale_guess = (1.72 * final_max) / (number_of_segments**2) # Current guess for the correct scale factor
scaler = (0.01 * final_max) / (number_of_segments**2) # Amount to adjust the scale factor guess by when last value of series is not equal to [final_max]
```
</br>
and test the two variations on different ranges and number of segments. This algorithm is fairly fast when only running off of one input - resulting in runtimes too small to see the difference in. To see the effect of the equation, we compound it by calling the solve function on a multitude of range sizes and number of segments and adding them all together. However, this still only shows us the effect on performance for one set of range sizes and number of segments. To reveal the true relationship between the equation and runtime performance, we call the solve function on a *multitude of* a multitude of range sizes and number of segments, and chart the runtime vs total number of tests for each multitude of range sizes and number of segments. </br>

![Figure_4](Figures/Figure_4.png) </br>

As you can see, the equation definitely enhances runtime. Even the slowest runtime using the equation is faster than the best runtime without it for the same number of tests. By finding the slope of the best fit line through each separate dataset, we can see that using the equation results in a runtime that is, on average, 55% faster than solving without the equation. This verifies again that our equation is correct while also giving us a more efficient means of finding the answer.
