 # Dempster-Shafer Theory Test
 # This script demonstrates the combination of evidence using Dempster-Shafer theory.
 # It combines two sources of evidence about the identities of individuals.  
 # Each source provides a basic probability assignment (mass function) for different hypotheses.


import matplotlib.pyplot as plt  # Import matplotlib for plotting results

 # Define basic probability assignments (mass functions) for sensor A
sensor_A = {
    frozenset(['Alice', 'Charlie']): 0.6,  # Belief that Alice is present: 60%
    frozenset(['Bob']): 0.3,    # Belief that Bob is present: 30%
    frozenset(['Alice', 'Bob']): 0.1  # Belief that either Alice or Bob is present: 10%
}

 # Define basic probability assignments (mass functions) for sensor B
sensor_B = {
    frozenset(['Bob', 'Alice']): 0.7,  # Belief that Bob is present: 70%
    frozenset(['Charlie', 'Alice']): 0.2,  # Belief that Charlie is present: 20%
    frozenset(['Bob', 'Charlie']): 0.1  # Belief that either Bob or Charlie is present: 10%
}

def combine_evidence(m1, m2):
    """
    Combines two mass functions using Dempster's rule of combination.
    m1, m2: dictionaries mapping frozenset hypotheses to their mass values.
    Returns: combined mass function as a dictionary.
    """
    combined = {}  # Dictionary to store combined mass assignments
    conflict = 0.0  # Variable to accumulate total conflict mass

    for A in m1:  # Iterate over all hypotheses in the first mass function
        for B in m2:  # Iterate over all hypotheses in the second mass function
            intersection = A & B  # Find intersection of hypotheses (common elements)
            mass = m1[A] * m2[B]  # Calculate joint mass for this pair
            if intersection:  # If intersection is not empty (compatible hypotheses)
                combined[intersection] = combined.get(intersection, 0) + mass  # Add mass to the intersection hypothesis
            else:  # If intersection is empty (conflicting hypotheses)
                conflict += mass  # Accumulate conflict mass

    # Normalize combined masses by dividing by (1 - total conflict)
    for key in combined:
        combined[key] /= (1 - conflict)

    return combined  # Return the normalized combined mass function

 # Combine the two sources of evidence using Dempster's rule
combined_belief = combine_evidence(sensor_A, sensor_B)

 # Display the results: print each hypothesis and its belief value
for hypothesis, belief in combined_belief.items():
    print(f"Hypothesis {set(hypothesis)}: Belief = {belief:.3f}")  # Show hypothesis as a set and belief rounded to 3 decimals

    # Prepare data for plotting
labels = [', '.join(hypothesis) for hypothesis in combined_belief]
beliefs = [belief for belief in combined_belief.values()]

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(labels, beliefs, color='skyblue', edgecolor='black')
plt.title('Combined Belief Distribution (Dempster–Shafer Theory)')
plt.xlabel('Hypotheses')
plt.ylabel('Belief Value')
plt.ylim(0, 1)

# Annotate bars with belief values
for bar, belief in zip(bars, beliefs):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
             f'{belief:.3f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()