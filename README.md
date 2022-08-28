# Increasing_Segmentation
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
