import streamlit as st

def determine_weather_type(degree):
    """Determine if the weather is 'cold' or 'hot'."""
    return 'hot' if degree > 22 else 'cold'

def compare_destinations(dest1_data, dest2_data, budget, weather_preference):
    """Compare two destinations and return a detailed report."""
    dest1_name, (cost1_sgd, weather1_degree, attractions1) = dest1_data
    dest2_name, (cost2_sgd, weather2_degree, attractions2) = dest2_data

    # Calculate price difference
    price_difference_sgd = abs(cost1_sgd - cost2_sgd)

    # Determine weather type
    weather_type1 = determine_weather_type(weather1_degree)
    weather_type2 = determine_weather_type(weather2_degree)

    # Calculate scores
    weather_score1 = 10 if weather_type1 == weather_preference else 0
    weather_score2 = 10 if weather_type2 == weather_preference else 0
    dest1_score = weather_score1 + attractions1
    dest2_score = weather_score2 + attractions2

    # Additional scoring
    if cost1_sgd <= budget:
        dest1_score += 1
    if cost2_sgd <= budget:
        dest2_score += 1
    if cost1_sgd < cost2_sgd:
        dest1_score += 1
    elif cost2_sgd < cost1_sgd:
        dest2_score += 1

    # Determine which destination is cheaper
    if cost1_sgd < cost2_sgd:
        cheaper_destination = f"{dest1_name} is cheaper than {dest2_name} by SGD {price_difference_sgd:.2f}"
    elif cost2_sgd < cost1_sgd:
        cheaper_destination = f"{dest2_name} is cheaper than {dest1_name} by SGD {price_difference_sgd:.2f}"
    else:
        cheaper_destination = "Both destinations have the same cost."

    return {
        "price_difference": price_difference_sgd,
        "weather_preference": weather_preference.capitalize(),
        "cost1": cost1_sgd,
        "cost2": cost2_sgd,
        "weather1": weather_type1.capitalize(),
        "weather2": weather_type2.capitalize(),
        "degree1": weather1_degree,
        "degree2": weather2_degree,
        "attractions1": attractions1,
        "attractions2": attractions2,
        "score1": dest1_score,
        "score2": dest2_score,
        "cheaper_destination": cheaper_destination
    }

def main():
    """Main function to run the Streamlit app."""
    st.title("AY's Travel Tally (Compare travel destinations)")

    # Get user preferences
    budget = st.number_input("Enter your budget in SGD:", min_value=0.0, format="%.2f")
    weather_preference = st.radio("Do you prefer 'cold' or 'warm' weather?", ('cold', 'warm'))

    # Input destination names
    dest1_name = st.text_input("Enter the name of Destination 1:")
    dest2_name = st.text_input("Enter the name of Destination 2:")

    # Input data for both destinations
    if dest1_name:
        cost1_sgd = st.number_input(f"Enter cost in SGD for {dest1_name}:", min_value=0.0, format="%.2f", key='cost1')
        weather1_degree = st.number_input(f"Enter the degree of {dest1_name}:", min_value=-100, max_value=100, key='weather1')
        attractions1 = st.slider(f"Enter attractions score (0-10) for {dest1_name}:", min_value=0.0, max_value=10.0, key='attractions1')

    if dest2_name:
        cost2_sgd = st.number_input(f"Enter cost in SGD for {dest2_name}:", min_value=0.0, format="%.2f", key='cost2')
        weather2_degree = st.number_input(f"Enter the degree of {dest2_name}:", min_value=-100, max_value=100, key='weather2')
        attractions2 = st.slider(f"Enter attractions score (0-10) for {dest2_name}:", min_value=0.0, max_value=10.0, key='attractions2')

    # Compare button
    if st.button("Compare Destinations"):
        if dest1_name and dest2_name:
            dest1_data = (dest1_name, (cost1_sgd, weather1_degree, attractions1))
            dest2_data = (dest2_name, (cost2_sgd, weather2_degree, attractions2))

            # Compare the destinations
            comparison_results = compare_destinations(dest1_data, dest2_data, budget, weather_preference)

            # Display comparison results
            st.subheader("Comparison Results:")
            st.write(f"Price Difference: SGD {comparison_results['price_difference']:.2f}")
            st.write(f"Preferred Weather: {comparison_results['weather_preference']}")
            st.write(f"{dest1_name} Cost: SGD {comparison_results['cost1']:.2f} (Within Budget: {comparison_results['cost1'] <= budget})")
            st.write(f"{dest2_name} Cost: SGD {comparison_results['cost2']:.2f} (Within Budget: {comparison_results['cost2'] <= budget})")
            st.write(f"{dest1_name} Weather: {comparison_results['weather1']} at {comparison_results['degree1']}°C")
            st.write(f"{dest2_name} Weather: {comparison_results['weather2']} at {comparison_results['degree2']}°C")
            st.write(f"{dest1_name} Attractions: {comparison_results['attractions1']}")
            st.write(f"{dest2_name} Attractions: {comparison_results['attractions2']}")
            st.write(f"{dest1_name} Score: {comparison_results['score1']}")
            st.write(f"{dest2_name} Score: {comparison_results['score2']}")
            st.write(comparison_results['cheaper_destination'])

            if comparison_results['score1'] > comparison_results['score2']:
                st.write(f"Recommendation: {dest1_name} is preferred.")
            elif comparison_results['score2'] > comparison_results['score1']:
                st.write(f"Recommendation: {dest2_name} is preferred.")
            else:
                st.write("Recommendation: Both destinations are equally preferred.")
        else:
            st.error("Please enter names for both destinations.")

if __name__ == "__main__":
    main()
