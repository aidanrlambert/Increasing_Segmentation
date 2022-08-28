# Generates a series of size [number_of_segments] such that second derivative of the series' values is always equal to [scale_factor]
def generateMaximums(scale_factor, number_of_segments):
    max_list = []
    i = 1
    while i <= number_of_segments:
        if i == 1:
            max_list.append(scale_factor)
        else:
            currentMax = (i) * scale_factor + max_list[i-2]
            max_list.append(currentMax)
        
        i += 1
    
    return max_list

# Finds the generateMaximum series and it's corresponding scale factor whose last value is equal to [final_max] given desired number of segments. 
# Accuracy adjusts the accuracy of last value == [final_max] check; Default 2 decimal places
def solve(final_max, number_of_segments, accuracy = 2):
    guess_maxes = [0] # Stored list of previous last values returned from generateMaximums
    scale_guess = 1.0 # Current guess for the correct scale factor
    scaler = 1.0 # Amount to adjust the scale factor guess by when last value of series is not equal to [final_max]

    # Make a first guess for scale factor. Used to set the initial direction of scaler
    maxes = generateMaximums(scale_guess, number_of_segments)
    guess_maxes.append(maxes[len(maxes) - 1])

    # While last value of generateMaximum series is not within [accuracy] decimal places of [final_max]
    while round(guess_maxes[len(guess_maxes) - 1], accuracy) != final_max:
        # If the previous last value found has been found before, decrease the scaler value to further tune scale factor guess.
        # When a last value has been found before, this indicates the function is alternating above and below [final_max]
        # and will not get any closer without changing the amount by which we adjust the scale factor guess by.
        if len(guess_maxes) > 3:
            if guess_maxes[len(guess_maxes) - 1] == guess_maxes[len(guess_maxes) - 3]:
                redux_factor = 0.1 # The amount by which to reduce the scaler

                # Find the next largest possible redux_factor that won't bring scaler too close to 0
                if scaler - redux_factor > 1e-15:
                    scaler -= redux_factor
                else:
                    while scaler - redux_factor <= 1e-15:
                        redux_factor /= 10
                    scaler -= redux_factor
        
        # If the previous last value of generateMaximum series was larger than [final_max], reduce scale factor guess by [scaler].
        # If the previous last value of generateMaximum series was smaller than [final_max], increase scale factor guess by [scaler].
        if guess_maxes[len(guess_maxes) - 1] > final_max:
            scale_guess -= scaler
        elif guess_maxes[len(guess_maxes) - 1] < final_max:
            scale_guess += scaler
        
        # Generate new series and append it's last value to [guess_maxes]
        maxes = generateMaximums(scale_guess, number_of_segments)
        guess_maxes.append(maxes[len(maxes) - 1])


    return scale_guess, maxes