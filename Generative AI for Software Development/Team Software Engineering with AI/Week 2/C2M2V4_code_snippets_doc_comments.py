# Example 1
def calculate_area(radius):
    """
    Calculate the area of a circle using the formula A = πr².

    Parameters:
    radius (float): Radius of the circle, should be non-negative.

    Returns:
    float: Area of the circle.

    Example:
    >>> calculate_area(5)
    78.53975
    """
    pi = 3.14159
    return pi * radius * radius


# Example 2
def find_max(numbers):
    """
    Find the maximum number in a list of numbers.

    Parameters:
    numbers (list): A list of numerical values.

    Returns:
    number: The largest number in the list.

    Example:
    >>> find_max([3, 1, 4, 1, 5, 9, 2, 6, 5])
    9

    Note:
    The list should contain at least one number. If the list is empty,
    the function will raise an IndexError.
    """
    max_number = numbers[0]
    for number in numbers:
        if number > max_number:
            max_number = number
    return max_number

# Example 3
def bubble_sort(arr):
    """
        Sort a list of numbers using the bubble sort algorithm.

        This function implements the bubble sort algorithm, which is a simple
        sorting technique. It repeatedly steps through the list, compares adjacent
        elements, and swaps them if they are in the wrong order. The process is
        repeated until the list is sorted.

        :param arr: A list of numbers to be sorted.
        :type arr: list

        :return: The sorted list of numbers.
        :rtype: list

        :Example:

        >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]

        :Note for C Programmers:
        - The `len(arr)` function is used to get the number of elements in the list,
          similar to using a loop to find the length of an array in C.
        - The `for` loop in Python is similar to a `for` loop in C, but it iterates
          over a range of numbers directly.
        - Swapping elements in Python can be done in one line using `arr[j], arr[j+1] = arr[j+1], arr[j]`,
          which is equivalent to using a temporary variable for swapping in C.
        - The function returns the sorted list, similar to how you might sort an array in-place in C.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr