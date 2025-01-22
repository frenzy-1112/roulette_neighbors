#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

def roulette_neighbors(number_neighbor_pairs):
    """
    Finds the neighbors of given numbers on a European Roulette wheel, each with its own neighbor count.

    Parameters:
        number_neighbor_pairs (list of tuples): A list where each tuple contains:
            - number (int): The number to find neighbors for (0-36).
            - neighbor_count (int): Number of neighbors on each side to include for this number.

    Returns:
        dict: A dictionary where keys are the given numbers, and values are lists of their neighbors.
    """
    roulette_wheel = [
        0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6,
        27, 13, 36, 11, 30, 8, 23, 10, 5, 24,
        16, 33, 1, 20, 14, 31, 9, 22, 18, 29,
        7, 28, 12, 35, 3, 26
    ]

    total_numbers = len(roulette_wheel)
    result = {}

    for number, neighbor_count in number_neighbor_pairs:
        if number not in roulette_wheel:
            raise ValueError(f"Invalid number: {number}. Must be between 0 and 36.")
        if neighbor_count < 0:
            raise ValueError(f"Neighbor count for number {number} must be non-negative.")

        index = roulette_wheel.index(number)

        neighbors = [
            roulette_wheel[(index + i) % total_numbers]
            for i in range(-neighbor_count, neighbor_count + 1)
        ]
        result[number] = neighbors

    return result

def parse_input(input_str, default_neighbors):
    """
    Parses user input in the format 'number count,number,...'
    Uses the default neighbor count if no count is specified.

    Parameters:
        input_str (str): The user input string.
        default_neighbors (int): The default neighbor count.

    Returns:
        list of tuples: Each tuple contains (number, neighbor_count).
    """
    pairs = input_str.split(',')
    number_neighbor_pairs = []
    for pair in pairs:
        parts = pair.strip().split()
        if len(parts) == 2:
            try:
                number = int(parts[0].strip())
                neighbor_count = int(parts[1].strip())
                number_neighbor_pairs.append((number, neighbor_count))
            except ValueError:
                raise ValueError(f"Invalid input format for pair '{pair}'. Ensure numbers and counts are integers.")
        elif len(parts) == 1:
            try:
                number = int(parts[0].strip())
                number_neighbor_pairs.append((number, default_neighbors))  # Use default neighbor count
            except ValueError:
                raise ValueError(f"Invalid number format for '{pair}'. Ensure it's an integer.")
        else:
            raise ValueError(f"Invalid format for '{pair}'. Use 'number count' or 'number'.")
    return number_neighbor_pairs

def plot_roulette_table(numbers):
    """
    Plots the roulette table with highlighted numbers.

    Args:
        numbers (list): A list of numbers to highlight.

    Returns:
        A Streamlit table object.
    """
    roulette_wheel = [
        [5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3],
        [10, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 26],
        [23, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32, 0],
    ]

    # Create a DataFrame
    df = pd.DataFrame(roulette_wheel)

    def highlight_numbers(val):
        if val in numbers:
            color = 'lightblue'  # Highlight color
        else:
            color = 'white'
        return f'background-color: {color}'

    # Apply the highlighting style
    styled_df = df.style.applymap(highlight_numbers)

    # Display the styled table in Streamlit
    return st.table(styled_df)

def main():
    st.title("Roulette Neighbors Finder")

    st.write(
        """Enter the numbers and their neighbors:
        
        Use the format: `number neighbor_count, number neighbor_count` or just `number` for a default neighbor count of 1.
        For example: `3 3, 8 1, 12`
        """
    )

    # Slider for default neighbor count, limited to 1 and 3
    default_neighbors = st.slider("Select default number of neighbors:", min_value=1, max_value=3, step=2, value=1)

    user_input = st.text_input("Input your numbers and neighbors:", "")

    if user_input:
        try:
            # Parse the user input with the default neighbor count
            number_neighbor_pairs = parse_input(user_input, default_neighbors)

            # Calculate the neighbors for the provided inputs
            neighbors = roulette_neighbors(number_neighbor_pairs)

            # Highlight only the input numbers
            input_numbers = [number for number, _ in number_neighbor_pairs]
            st.subheader("Table 1: Input Numbers Only")
            plot_roulette_table(input_numbers)

            # Highlight input numbers and their neighbors
            numbers_to_highlight = []
            for neighbor_list in neighbors.values():
                numbers_to_highlight.extend(neighbor_list)
            numbers_to_highlight = list(set(numbers_to_highlight))  # Remove duplicates

            st.subheader("Table 2: Input Numbers and Neighbors")
            plot_roulette_table(numbers_to_highlight)

        except ValueError as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
