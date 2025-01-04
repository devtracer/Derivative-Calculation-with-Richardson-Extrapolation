# Introduction

This Python code creates a graphical user interface (GUI) using the `customtkinter` library to calculate the first derivative of a mathematical function 
at a given point using Richardson extrapolation. It also allows the user to plot the function and its derivative.

# How To Install?

1. Download the main.py file

2. Run this command on your terminal:
   - for Linux:
        ```
         python -m pip install tk customtkinter numpy sympy matplotlib
        ```
   - for Windows:
        ```
         pip install tk customtkinter numpy sympy matplotlib
        ```

3. Run the main.py file.


# Explanations

The key components and steps in the code are as follows:

1. **Libraries Import:**
   - `customtkinter` (ctk): Used for creating the custom-styled Tkinter GUI elements.
   - `numpy` (np): Used for numerical operations, such as creating arrays and computing function values.
   - `sympy` (sp): Used for symbolic math, particularly to parse mathematical expressions and calculate derivatives.
   - `tkinter`: Standard GUI library for Python (used indirectly via customtkinter).
   - `matplotlib.pyplot`: Used for plotting the function and its derivative.
   - `FigureCanvasTkAgg`: Used to embed matplotlib plots into the Tkinter window.

2. **Functions:**
   - **richardson_extrapolation(func, x, h, tol, max_iter):**
     This function computes the derivative of a given function using Richardson extrapolation. It iteratively improves the accuracy of the derivative by refining the step size `h`. The stopping condition is based on the tolerance `tol`.

     Here's the richardson extrapolation code:

    ![image](https://github.com/user-attachments/assets/9ee557f3-ca41-41af-9cb6-0a04d362aebb)

   
   - **parse_function(expr):**
     This function parses the mathematical expression entered by the user. It replaces numpy function calls with their sympy equivalents and converts the expression into a sympy expression that can be evaluated numerically.
   
   - **calculate_derivative():**
     This function handles user inputs, including the mathematical expression, x-value, step size `h`, and tolerance. It then calculates the derivative using Richardson extrapolation and displays the result in the GUI. It also triggers the plot function to show the function and its derivative.

   - **plot_function_and_derivative(func, x, h):**
     This function generates the plot of the function and its derivative. It uses numpy to create a range of x-values and calculates the function values and derivative approximations using Richardson extrapolation. It then displays the plot in the Tkinter window.

3. **GUI Components:**
   - The GUI is created using `customtkinter`, which enhances the default Tkinter widgets with modern designs.
   - Users can input the function, the point at which they want to calculate the derivative (`x`), the step size (`h`), and the tolerance (`tol`).
   - After entering the required inputs, the user can click a button to calculate the derivative. The result is shown in the GUI, and a plot of the function and its derivative is displayed.
