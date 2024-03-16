import plotly.express as px
import numpy as np

# Define the callback to update the second dropdown based on the first dropdown selection
def update_dropdown_b_options(selected_option, options):
    return [{'label': i, 'value': i} for i in options[selected_option]]

# Define the callback to update the plot based on both dropdown selections
def update_plot(selected_option_a, selected_option_b):
    if selected_option_a == 'A':
        # Scatter plot
        fig = px.scatter(
            x=np.random.rand(100), 
            y=np.random.rand(100), 
            title=f"Option {selected_option_a} - Suboption {selected_option_b}"
        )

    elif selected_option_a == 'B':
        # Bar chart
        fig = px.bar(
            x=['A', 'B', 'C'], 
            y=np.random.randint(1, 10, size=3), 
            title=f"Option {selected_option_a} - Suboption {selected_option_b}"
        )
    
    elif selected_option_a == 'C':
        # Line chart
        x = np.linspace(0, 10, 1000)
        
        omega = np.random.randint(1, 10)
        y = np.sin(omega*x)
        
        fig = px.line(
            x=x, y=y, 
            title=f"Option {selected_option_a} - Suboption {selected_option_b}"
        )
    
    return fig