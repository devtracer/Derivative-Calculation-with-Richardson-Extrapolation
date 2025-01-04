import customtkinter as ctk
import numpy as np
import sympy as sp
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate the first derivative using Richardson extrapolation
def richardson_extrapolation(func, x, h, tol=1e-6, max_iter=20):
    R = np.zeros((max_iter, max_iter))  # Matrix to store extrapolation values
    for i in range(max_iter):
        step = h / (2 ** i)  # Reducing step size by a factor of 2 with each iteration
        # Central difference formula for derivative approximation
        R[i, 0] = (func(x + step) - func(x - step)) / (2 * step)
        for k in range(1, i + 1):
            # Richardson extrapolation step to improve the accuracy
            R[i, k] = (4 ** k * R[i, k - 1] - R[i - 1, k - 1]) / (4 ** k - 1)
        # Stop if the result converges (i.e., the difference between successive iterations is less than tolerance)
        if i > 0 and abs(R[i, i] - R[i - 1, i - 1]) < tol:
            return R[i, i]
    raise ValueError("Desired accuracy not achieved.")

# Function to parse the user input function expression and replace numpy functions with sympy equivalents
def parse_function(expr):
    try:
        expr = expr.replace("np.", "")  # Remove numpy prefix to make it compatible with sympy
        x = sp.symbols('x')  # Define 'x' as a symbol for symbolic computation
        parsed_expr = sp.sympify(expr)  # Convert the input string to a sympy expression
        return parsed_expr
    except Exception as e:
        raise ValueError(f"Invalid function or input: {str(e)}")

# Function to calculate the derivative and display the result
def calculate_derivative():
    try:
        # Retrieve the user inputs
        func_expr = function_input.get()
        x_val = float(x_input.get())
        h_val = float(h_input.get())
        tol_val = float(tol_input.get())

        # Parse the function expression using sympy
        parsed_expr = parse_function(func_expr)

        # Convert the sympy expression to a function that can be evaluated numerically
        x = sp.symbols('x')
        func = sp.lambdify(x, parsed_expr, "numpy")

        # Calculate the derivative using Richardson extrapolation
        result = richardson_extrapolation(func, x_val, h_val, tol_val)

        # Clear any previous result in the result frame
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Display the result in the GUI
        result_label = ctk.CTkLabel(result_frame, text=f"The derivative of the function at x={x_val} is: {result:.10f}", font=("Arial", 14))
        result_label.pack(pady=10)

        # Plot the function and its derivative
        plot_function_and_derivative(func, x_val, h_val)

    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

# Function to plot the function and its derivative
def plot_function_and_derivative(func, x, h):
    # Clear any previous plot in the plot frame
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Generate x values for the plot
    x_vals = np.linspace(x - 2, x + 2, 400)
    y_vals = func(x_vals)  # Calculate function values for the plot

    # Compute the derivative using Richardson extrapolation for each x value
    derivative_vals = np.array([richardson_extrapolation(func, xi, h) for xi in x_vals])

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.plot(x_vals, y_vals, label="Function", color='blue')  # Plot the function
    ax.plot(x_vals, derivative_vals, label="Derivative", color='red', linestyle='--')  # Plot the derivative

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Function and its Derivative')
    ax.legend()

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

# Set up the appearance mode and theme for the GUI
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Blue theme

# Create the main window
root = ctk.CTk()
root.title("Derivative Calculation with Richardson Extrapolation")
root.geometry("1920x1080")

# Create a frame for the input fields
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Function input field
function_label = ctk.CTkLabel(frame, text="Enter the function (e.g., np.sin(x) * np.cos(x) * x**2)", font=("Arial", 14))
function_label.grid(row=0, column=0, padx=10, pady=5)
function_input = ctk.CTkEntry(frame, width=300, font=("Arial", 14))
function_input.insert(0, "np.sin(x) * np.cos(x) * x**2")  # Default function
function_input.grid(row=0, column=1, padx=10, pady=5)

# x value input field
x_label = ctk.CTkLabel(frame, text="Enter x value (e.g., 2)", font=("Arial", 14))
x_label.grid(row=1, column=0, padx=10, pady=5)
x_input = ctk.CTkEntry(frame, width=300, font=("Arial", 14))
x_input.insert(0, "2")  # Default x value
x_input.grid(row=1, column=1, padx=10, pady=5)

# h value input field
h_label = ctk.CTkLabel(frame, text="Enter step size (h, e.g., 0.01)", font=("Arial", 14))
h_label.grid(row=2, column=0, padx=10, pady=5)
h_input = ctk.CTkEntry(frame, width=300, font=("Arial", 14))
h_input.insert(0, "0.01")  # Default step size
h_input.grid(row=2, column=1, padx=10, pady=5)

# Tolerance input field
tol_label = ctk.CTkLabel(frame, text="Enter tolerance (tol, e.g., 1e-6)", font=("Arial", 14))
tol_label.grid(row=3, column=0, padx=10, pady=5)
tol_input = ctk.CTkEntry(frame, width=300, font=("Arial", 14))
tol_input.insert(0, "1e-6")  # Default tolerance value
tol_input.grid(row=3, column=1, padx=10, pady=5)

# Button to calculate the derivative
calculate_button = ctk.CTkButton(root, text="Calculate Derivative", command=calculate_derivative, font=("Arial", 14))
calculate_button.pack(pady=20)

# Frame for displaying the plot
plot_frame = ctk.CTkFrame(root)
plot_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Frame for displaying the result
result_frame = ctk.CTkFrame(root)
result_frame.pack(pady=10, padx=20)

# Instructions label for the function input
instructions_label = ctk.CTkLabel(root, text="Instructions on entering functions:\n"
                                              "1. Use 'np' for numpy functions, e.g., np.sin(x), np.cos(x), np.log(x), etc.\n"
                                              "2. Use '**' for exponents, e.g., x**2 for x squared.\n"
                                              "3. Avoid using regular mathematical notation like '12x^2'; instead, write '12*x**2'.\n"
                                              "4. For natural logarithm, use 'np.log(x)'.\n"
                                              "Example: np.sin(x) * np.cos(x) * x**2", 
                                              font=("Arial", 12), anchor="w", justify="left")
instructions_label.pack(pady=10, padx=20)

# Explanation label for x, h, and tol input values
values_label = ctk.CTkLabel(root, text="How to Enter x, h, and tol Values:\n"
                                       "1. 'x' is the point at which you want to calculate the derivative. For example, enter '2' or '3.0'.\n"
                                       "2. 'h' is the step size, which controls the accuracy of the derivative approximation. For example, '0.01'.\n"
                                       "3. 'tol' is the tolerance level, which determines when to stop iterating. For example, '1e-6' or '1e-8'.",
                                       font=("Arial", 12), anchor="w", justify="left")
values_label.pack(pady=10, padx=20)

# Run the GUI application
root.mainloop()
