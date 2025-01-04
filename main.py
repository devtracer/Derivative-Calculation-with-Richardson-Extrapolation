import customtkinter as ctk
import numpy as np
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def richardson_extrapolation(func, x, h, tol=1e-6, max_iter=20):
    """
    Calculate the first derivative using Richardson extrapolation.
    """
    R = np.zeros((max_iter, max_iter))
    for i in range(max_iter):
        step = h / (2 ** i)
        R[i, 0] = (func(x + step) - func(x - step)) / (2 * step)
        for k in range(1, i + 1):
            R[i, k] = (4 ** k * R[i, k - 1] - R[i - 1, k - 1]) / (4 ** k - 1)
        if i > 0 and abs(R[i, i] - R[i - 1, i - 1]) < tol:
            return R[i, i], R  # Return the result and the table of extrapolations
    raise ValueError("Desired accuracy not achieved.")

def evaluate_expression(expr, x):
    """Convert the input string to a function and evaluate it."""
    try:
        # Safely evaluate the expression, allowing for numpy functions
        return eval(expr, {"x": x, "np": np, "np.exp": np.exp, "np.log": np.log, "np.sin": np.sin, "np.cos": np.cos, "np.tan": np.tan})
    except Exception as e:
        raise ValueError(f"Invalid function or input: {str(e)}")

def calculate_derivative():
    """Calculate the derivative and display the result along with the table and plot."""
    try:
        func_expr = function_input.get()
        x_val = float(x_input.get())
        h_val = float(h_input.get())
        tol_val = float(tol_input.get())

        # Convert the string function to a computable function
        func = lambda x: evaluate_expression(func_expr, x)

        # Calculate the derivative and the extrapolation table
        result, table = richardson_extrapolation(func, x_val, h_val, tol_val)

        # Display the derivative result in the GUI
        result_label.configure(text=f"The derivative of the function at x={x_val} is: {result:.10f}")

        # Display the extrapolation table
        display_extrapolation_table(table)

        # Plotting the function and its derivative
        plot_function_and_derivative(func, x_val, h_val, table)

    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def plot_function_and_derivative(func, x, h, table):
    """Plot the function and its derivative."""
    # Generate x values and corresponding function values
    x_vals = np.linspace(x - 2, x + 2, 400)
    y_vals = np.vectorize(func)(x_vals)

    # Compute derivative approximation using Richardson extrapolation for each x
    derivative_vals = np.array([richardson_extrapolation(func, xi, h)[0] for xi in x_vals])

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.plot(x_vals, y_vals, label="Function", color='blue')
    ax.plot(x_vals, derivative_vals, label="Derivative", color='red', linestyle='--')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Function and its Derivative')
    ax.legend()

    # Display the plot in the Tkinter window
    for widget in plot_frame.winfo_children():
        widget.destroy()  # Remove previous plot
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

def display_extrapolation_table(table):
    """Display the Richardson extrapolation table."""
    # Convert the table into a pandas DataFrame for better display
    df = pd.DataFrame(table)
    
    # Update table label content and ensure it's not destroyed
    table_label.configure(text="Richardson Extrapolation Table")

    # Clear the table frame but keep the label
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Create and display the new table in the Tkinter window
    table_text = df.to_string(index=False, header=True)
    table_label.configure(text=table_text)

# Initial customtkinter settings
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Blue theme

# Create the main window
root = ctk.CTk()
root.title("Derivative Calculation with Richardson Extrapolation")
root.geometry("700x800")

# Create a frame for inputs to keep them organized
frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=20, fill="both", expand=True)

# Function input
function_label = ctk.CTkLabel(frame, text="Enter the function (e.g., np.sin(x))", font=("Arial", 14))
function_label.grid(row=0, column=0, padx=10, pady=5)
function_input = ctk.CTkEntry(frame, width=300, font=("Arial", 14))
function_input.grid(row=0, column=1, padx=10, pady=5)
# Set default value for function input
function_input.insert(0, "np.sin(x)")

# x value input
x_label = ctk.CTkLabel(frame, text="Enter x value (e.g., 1.5)", font=("Arial", 14))
x_label.grid(row=1, column=0, padx=10, pady=5)
x_input = ctk.CTkEntry(frame, width=300, font=("Arial", 14))
x_input.grid(row=1, column=1, padx=10, pady=5)
# Set default value for x input
x_input.insert(0, "1.5")

# h value input
h_label = ctk.CTkLabel(frame, text="Enter step size (h, e.g., 0.01)", font=("Arial", 14))
h_label.grid(row=2, column=0, padx=10, pady=5)
h_input = ctk.CTkEntry(frame, width=300, font=("Arial", 14))
h_input.grid(row=2, column=1, padx=10, pady=5)
# Set default value for h input
h_input.insert(0, "0.01")

# tol value input
tol_label = ctk.CTkLabel(frame, text="Enter tolerance (tol, e.g., 1e-6)", font=("Arial", 14))
tol_label.grid(row=3, column=0, padx=10, pady=5)
tol_input = ctk.CTkEntry(frame, width=300, font=("Arial", 14))
tol_input.grid(row=3, column=1, padx=10, pady=5)
# Set default value for tol input
tol_input.insert(0, "1e-6")

# Derivative calculation button
calculate_button = ctk.CTkButton(root, text="Calculate Derivative", command=calculate_derivative, font=("Arial", 14))
calculate_button.pack(pady=20)

# Create a frame for the results
result_frame = ctk.CTkFrame(root)
result_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Label for showing the result
result_label = ctk.CTkLabel(result_frame, text="Derivative Result will appear here.", font=("Arial", 14))
result_label.pack(pady=5)

# Create a frame for the table
table_frame = ctk.CTkFrame(root)
table_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Label for showing the extrapolation table
table_label = ctk.CTkLabel(table_frame, text="Richardson Extrapolation Table", font=("Arial", 14))
table_label.pack(pady=5)

# Create a frame for plotting
plot_frame = ctk.CTkFrame(root)
plot_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Instruction text for how to enter functions
instructions_label = ctk.CTkLabel(root, text="Instructions on entering functions:\n"
                                              "1. Use 'np' for numpy functions, e.g., np.sin(x), np.cos(x), np.log(x), etc.\n"
                                              "2. Use '**' for exponents, e.g., x**2 for x squared.\n"
                                              "3. Avoid using regular mathematical notation like '12x^2'; instead, write '12*x**2'.\n"
                                              "4. For natural logarithm, use 'np.log(x)'.\n"
                                              "Example: np.sin(x) + np.log(x) + x**2", 
                                              font=("Arial", 12), anchor="w", justify="left")
instructions_label.pack(pady=10, padx=20)

# Explanation for x, h, and tol values
values_label = ctk.CTkLabel(root, text="How to Enter x, h, and tol Values:\n"
                                       "1. 'x' is the point at which you want to calculate the derivative. For example, enter '1.5' or '3.0'.\n"
                                       "2. 'h' is the step size, which controls the accuracy of the derivative approximation. For example, '0.01'.\n"
                                       "3. 'tol' is the tolerance level, which determines when to stop iterating. For example, '1e-6' or '1e-8'.",
                                       font=("Arial", 12), anchor="w", justify="left")
values_label.pack(pady=10, padx=20)

# Run the program
root.mainloop()
