import numpy as np

def get_escape_time(c: complex, max_iterations: int) -> int | None:
    z = c
    for i in range(max_iterations+1):  # to include max_iterations
        if abs(z) > 2:  # After more than two, escape
            return i
        z = z * z + c  # Mandelbrot relation

    return None  # if it never escaped

def get_complex_grid(top_left: complex, bottom_right: complex, step: float) -> np.ndarray:
    real_start = top_left.real
    real_end = bottom_right.real   # Extract real and imaginary parts from the complex numbers
    imaginary_start = top_left.imag
    imaginary_end = bottom_right.imag

    real_values = np.arange(real_start, real_end, step)
    imaginary_values = np.arange(imaginary_start, imaginary_end, -step)  # Negative step for decreasing imaginary part

    real_grid = real_values[np.newaxis, :]  # use broadcast to expand real_values to the length of real part
    #np.newaxis is a special constant in NumPy that inserts a new dimension (axis) at a specified position in the array.
    #First insert the new dimension (np.newaxis), then select all columns (:)

    imaginary_grid = imaginary_values[:, np.newaxis]  # expand imag_values to the length of image part

    # Combine real and imaginary parts
    final_grid = real_grid + 1j * imaginary_grid

    return final_grid

def get_escape_time_color_arr(c_arr: np.ndarray, max_iterations: int) -> np.ndarray:
    """
    :param c_arr: numpy array of complex values that represent points on a complex array
    :param max_iterations: maximum number of iterations
    :return: numpy array the same shape as c_arr with the greyscale values
    """
    # Set z to the numpy array with the same shape as c_arr, initialized to 0
    z = np.zeros(c_arr.shape, dtype= complex)
    # Create an array of ones to store escape times, initialized to max_iterations + 1
    escape_time = np.ones(c_arr.shape, dtype=int) * (max_iterations + 1)
    #track which haven't escaped
    mask= np.ones(c_arr.shape, dtype=bool)

    # Loop through each point to check when they escape
    for i in range(1, max_iterations + 1):
        #formula
        z[mask] = z[mask] ** 2 + c_arr[mask]

        #points that have now escaped
        escaped = mask & (np.abs(z) > 2)
        #assigning escape times
        escape_time[escaped]= i
        #stops updating the points
        mask[escaped] = False

    # Set the color based on when each point escaped
    color_arr = (max_iterations - escape_time + 1) / (max_iterations + 1)

    # Return the color array to create the image
    return color_arr

def get_julia_color_arr(grid: np.ndarray, c: complex, max_iterations: int ) -> np.ndarray:
    """
        Parameters:
        grid (np.array):
            A 2D NumPy array of complex numbers representing the grid.
        c (complex):
            The complex parameter for the Julia set.
        max_iterations (int):
            The maximum number of iterations.

        Returns:
        np.array: An array containing the escape iteration for each point in the grid.
    """
    #algorithm very similar to get_escape_time_color_arr
    escape_time = np.ones(grid.shape, dtype=int) * (max_iterations + 1)
    mask = np.ones(grid.shape, dtype=bool)
    z = grid.copy()

    for i in range(1, max_iterations + 1):
        z[mask] = z[mask] ** 2 + c
        escaped = np.abs(z) > max(abs(c), 2)
        escape_time[mask & escaped] = i
        mask[escaped] = False

    julia_color = (max_iterations - escape_time + 1) / (max_iterations + 1)

    return julia_color
