from fractions import Fraction
from IPython.display import display, Math
import numpy as np


def float_to_fraction_latex(number,
                            tolerance=1e-6) -> tuple[bool, str]:
    # Convert the float to a Fraction
    fraction = Fraction(number).limit_denominator()
    
    # Check if the conversion is close enough to the original number
    if abs(fraction - number) < tolerance:
        return True, f"\\frac{{{fraction.numerator}}}{{{fraction.denominator}}}"
    else:
        return False, f"{number:.2f}"


def mtolat(matrix: np.ndarray | np.matrix, bl_frac: bool = True, augmented: bool = False) -> str:
    latex_str = "\\begin{bmatrix}\n"
    for row in matrix:
        if isinstance(row, np.ndarray):
            row= np.array(row).flatten()
        blfracline = False
        blfrac = False
        for i, elem in enumerate(row):
            if i == len(row) - 1 and augmented:
                latex_str += " | "
            if isinstance(elem, int):
                latex_str += f" {int(elem)} &"
            if elem == 0:
                latex_str += f" 0 &"
            elif isinstance(elem, str):
                latex_str += f"{elem} &"
            elif elem - int(elem) == 0:
                latex_str += f"{int(elem)} &"
            elif isinstance(elem, float):
                if bl_frac:
                    blfrac, elem = float_to_fraction_latex(elem)
                else:
                    elem = f"{elem:.2f}"
                latex_str += f"{elem} &"
            else:
                raise ValueError(f"Element {elem} is not an integer or float.")
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
         " ": r"\,", "  ": r"\quad", "   ": r"\qquad",
         "->": r"\rightarrow", "<-": r"\leftarrow",
         "-->": r"\longrightarrow", "<--": r"\longleftarrow"}

def printalg(*args, debug=False, blfrac=True):
    """Prints a list of strings and matrices in LaTeX format. The matrices are printed in a bmatrix environment.

    Args:
        *args: A list of strings or matrices, these are specific commands:
            - "@" is replaced by "\cdot"
            - "frac" is replaced by "\frac"
            - "[" is replaced by "\left["
            - "]" is replaced by "\right]"
            - "(" is replaced by "\left("
            - ")" is replaced by "\right)"
            - " " is replaced by "\,"
            - "  " is replaced by "\quad"
            - "   " is replaced by "\qquad"
            - "->" is replaced by "\rightarrow"
            - "<-" is replaced by "\leftarrow"
            - "-->" is replaced by "\longrightarrow"
            - "<--" is replaced by "\longleftarrow"
            - If the string "aug" precedes a matrix, the matrix is considered augmented
                so if you run:
                    printalg("aug", np.array([[1, 2, 5], [3, 4, 6]]))
                you will get:
                    \begin{bmatrix}
                        1 & 2 &| 5 \\
                        3 & 4 &| 6 \\
                    \end{bmatrix}
        debug: If True, the LaTeX code is printed.
        blfrac: If True, the fractions are printed as fractions in the LaTeX code.
    """
    txt = ""
    bl_aug = False
    for arg in args:
        if isinstance(arg, str):
            if arg == "aug":
                bl_aug = True
                continue
            ss = arg
            for k, v in d_sub.items():
                ss = ss.replace(k, v)
            txt += ss
        elif isinstance(arg, np.ndarray) or isinstance(arg, np.matrix) or isinstance(arg, list):
            if bl_aug and isinstance(arg, np.matrix):
                txt += mtolat(arg, bl_frac=blfrac, augmented=True)
                bl_aug = False
                continue
            if isinstance(arg, list):
                if not isinstance(arg[0], list):
                    continue
            txt += mtolat(arg, bl_frac=blfrac)
        else:
            raise ValueError(f"Argument {arg} is not a string or a matrix.")
    if debug:
        print(txt)
    display(Math(txt))