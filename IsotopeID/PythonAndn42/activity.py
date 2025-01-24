import math

# Function to calculate the decay constant from the half-life
def decay_constant(half_life):
    # Half-life is in seconds
    return math.log(2) / half_life

# Function to calculate the activity A(t) at a given time t
def activity(A0, decay_constant, time):
    # Use the formula A(t) = A0 * e^(-lambda * t)
    return A0 * math.exp(-decay_constant * time)

# Function to convert years to seconds
def years_to_seconds(years):
    return years * 365 * 24 * 3600

# Main function to execute the calculation
def main():
    # Given values
    initial_activity = 428.2  # in kBq (initial activity)
    half_life_years = 30.07  # in years
    initial_time_years = 0  # initial time in years (usually 0)
    final_time_years = 34.9358260256  # final time to calculate activity after 5 years
    
    # Step 1: Convert the half-life from years to seconds
    half_life_seconds = years_to_seconds(half_life_years)
    
    # Step 2: Calculate the decay constant (lambda)
    lambda_value = decay_constant(half_life_seconds)
    
    # Step 3: Convert the final time from years to seconds
    final_time_seconds = years_to_seconds(final_time_years)
    
    # Step 4: Calculate the activity at the final time t using the formula A(t) = A0 * e^(-lambda * t)
    activity_value = activity(initial_activity, lambda_value, final_time_seconds)
    
    # Output the results
    print(f"Decay constant (λ): {lambda_value:.3e} s^-1")
    print(f"Activity after {final_time_years} years: {activity_value:.3e} kBq")

# Run the program
if __name__ == "__main__":
    main()
