# DFA String Matcher: Malaysian Cuisine Edition

This Python script implements a Deterministic Finite Automaton (DFA) string matching algorithm to scan a text file (`sample.txt`) and identify occurrences of various traditional Malaysian foods and beverages.

## Overview

The program reads a target text and searches for a predefined list of keywords (Malaysian dishes like "Nasi Lemak", "Teh tarik", "Roti canai", etc.). It utilizes a DFA-based approach, which processes the text character by character, transitioning through states to find matches.

When the script runs, it outputs:
1.  **Summary:** A count of how many times each specific food word was found, along with its exact starting index in the text.
2.  **Visualized Text:** The original text printed to the console with all found food keywords highlighted in **bold**.

## Prerequisites

* Python 3.x installed on your machine.
* A terminal or command prompt that supports ANSI escape codes (for the bold text highlighting to work properly).

## File Structure

* `main.py` (or whatever you named the script): The main Python script containing the DFA logic.
* `sample.txt`: The text file that the script will read and scan for keywords. **(You must create this file and place it in the same directory as the script).**

## How to Run

1.  **Clone or Download:** Ensure both the Python script and `sample.txt` are in the same folder.
2.  **Prepare the Sample Text:** Add some text to `sample.txt`. For example:
    ```text
    Yesterday I went to the mamak stall and ordered a plate of Nasi Lemak and some Roti canai. To drink, I had a hot Teh tarik. It was delicious! Later, for dessert, we grabbed some Cendol.
    ```
3.  **Execute the Script:** Open your terminal, navigate to the directory containing the files, and run:
    ```bash
    python your_script_name.py
    ```
    *(Replace `your_script_name.py` with the actual name of your Python file).*

## How the Algorithm Works (DFA)

The core of the string matching is handled by the `run_dfa` and `transition` functions.

1.  **State Initialization:** For every word in the search list, the script initializes a state starting at `0`.
2.  **Character Iteration:** The script iterates through the input text character by character.
3.  **State Transitions:** For each character, the `transition` function determines the next state for every target word.
    * If the current character matches the expected character of a target word (case-insensitive), the state advances (`state + 1`).
    * If the state reaches the length of the word, a full match is recorded, and the state resets to `0`.
    * If there is a mismatch, the state resets. The script includes logic to handle overlapping characters (e.g., if a mismatch occurs, it checks if the current character could be the *start* of the word).

## Customization

You can easily modify the script to search for different keywords or scan different files:

* **Change the Target File:** Update the filename in the `read_file("sample.txt")` call.
* **Change the Keywords:** Modify the `list_of_words` array in the script to include the words you want to search for.

## Note on Output Formatting

The `print_bolded_text` function uses ANSI escape sequences (`\033[1m` for bold, `\033[0m` to reset) to format the console output. If your terminal does not support these sequences, you may see strange characters instead of bold text. Most modern terminals (like Windows Terminal, macOS Terminal, and Linux emulators) support this by default.
