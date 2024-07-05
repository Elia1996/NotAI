from fractions import Fraction
from IPython.display import display, Math
import numpy as np


def float_to_fraction_latex(number,
                            tolerance=1e-6) -> tuple[bool, str]:
    # Convert the float to a Fraction
    fraction = Fraction(number).limit_denominator()
    
    # Check if the conversion is close enough to the original number
    if number == 0:
        return True, "0"
    elif abs(fraction - number) < tolerance:
        return True, f"\\frac{{{fraction.numerator}}}{{{fraction.denominator}}}"
    else:
        return False, f"{number:.2f}"


def mtolat(matrix: np.ndarray | np.matrix, bl_frac: bool = True) -> str:
    latex_str = "\\begin{bmatrix}\n"
    for row in matrix:
        if isinstance(row, np.ndarray):
            row= np.array(row).flatten()
        blfracline = False
        blfrac = False
        for elem in row:
            if isinstance(elem, int):
                latex_str += f" {elem} &"
            elif isinstance(elem, float):
                if bl_frac:
                    blfrac, elem = float_to_fraction_latex(elem)
                else:
                    elem = f"{elem:.2f}"
                latex_str += f"{elem} &"
            else:
                latex_str += f" {elem} &"
            blfracline = blfracline or blfrac
        latex_str = latex_str[:-2] + "\\\\"
        if blfracline:
            latex_str += "[6pt]"
        latex_str += "\n"
    latex_str += "\\end{bmatrix}"
    return latex_str

d_sub = {"@": r"\cdot", "frac": r"\frac",
         "[": r"\left[", "]": r"\right]",
         "(": r"\left(", ")": r"\right)",
         " ": r"\,", "  ": r"\quad", "   ": r"\qquad"}

def printalg(*args, debug=False, blfrac=True):
    txt = ""
    for arg in args:
        if isinstance(arg, str):
            ss = arg
            for k, v in d_sub.items():
                ss = ss.replace(k, v)
            txt += ss
        elif isinstance(arg, np.ndarray):
            txt += mtolat(arg, bl_frac=blfrac)
    if debug:
        print(txt)
    display(Math(txt))