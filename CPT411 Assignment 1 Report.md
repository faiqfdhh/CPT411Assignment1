---
title: "CPT411 Assignment 1 – Food Finder DFA"
subtitle: "L4: Deterministic Finite Automaton for Malaysian Food Recognition"
date: "2026"
---

# I. Introduction

## 1.1 Language Definition

This project implements a **Deterministic Finite Automaton (DFA)** for **Language L4: Food Finder**. The DFA is designed to identify and extract Malaysian food names from a given text by processing one character at a time from left to right.

The language is defined as:

$$L = \{w \in \Sigma^* \mid w \text{ contains a substring matching any Malaysian food name as a whole word}\}$$

where $\Sigma = \{a, \ldots, z,\ A, \ldots, Z,\ 0, \ldots, 9,\ \text{and other symbols found in the text}\}$.

The DFA searches for **140+ Malaysian food patterns** including dishes such as *Nasi Lemak*, *Roti Canai*, *Laksa*, *Rendang*, *Satay*, and many others spanning categories like staple foods, main dishes, soups, desserts, drinks, and condiments.

## 1.2 Scope

The program performs **whole-word, case-insensitive matching**. A pattern is only accepted when it appears as a complete word — that is, bounded by non-alphabetic characters (or the start/end of the text) on both sides. This prevents false matches such as matching "Mi" inside the word "Malaysia".

## 1.3 DFA Definition

The DFA for each pattern $p = p_1 p_2 \ldots p_n$ of length $n$ is formally defined as the 5-tuple $(Q, \Sigma, \delta, q_0, F)$:

- **States:** $Q = \{q_0, q_1, q_2, \ldots, q_n, q_{trap}\}$
- **Alphabet:** $\Sigma = \{a, \ldots, z,\ A, \ldots, Z,\ 0, \ldots, 9,\ \text{space, punctuation, etc.}\}$
- **Start state:** $q_0$ (BOUNDARY — at a word boundary)
- **Accept state:** $F = \{q_n\}$ (all characters of the pattern have been matched; acceptance is confirmed when the next character is a word boundary)
- **Trap state:** $q_{trap}$ (inside a non-matching word; no valid transition until the next word boundary)

## 1.4 Transition Function

The transition function $\delta(q, c)$ is defined as follows:

| Current State | Input Character $c$ | Next State | Description |
|---|---|---|---|
| $q_0$ (BOUNDARY) | $c$ matches $p_1$ (case-insensitive) | $q_1$ | Start matching pattern |
| $q_0$ (BOUNDARY) | $c$ is alphabetic but does not match $p_1$ | $q_{trap}$ | Wrong word, enter trap |
| $q_0$ (BOUNDARY) | $c$ is non-alphabetic | $q_0$ | Stay at boundary |
| $q_i$ $(1 \leq i < n)$ | $c$ matches $p_{i+1}$ (case-insensitive) | $q_{i+1}$ | Continue matching |
| $q_i$ $(1 \leq i < n)$ | $c$ is alphabetic but does not match | $q_{trap}$ | Mismatch, enter trap |
| $q_i$ $(1 \leq i < n)$ | $c$ is non-alphabetic | $q_0$ | Partial match broken, reset |
| $q_n$ (ACCEPT) | $c$ is non-alphabetic | $q_0$ | **Match confirmed** |
| $q_n$ (ACCEPT) | $c$ is alphabetic | $q_{trap}$ | Not a whole word, reject |
| $q_{trap}$ | $c$ is non-alphabetic | $q_0$ | Reset at boundary |
| $q_{trap}$ | $c$ is alphabetic | $q_{trap}$ | Stay trapped |

## 1.5 Sample DFA — Pattern "Laksa"

Since the complete DFA for all 140+ patterns is too large to display, below is a sample DFA for the pattern **"Laksa"** ($n = 5$, states $q_0$ through $q_5$ plus $q_{trap}$):

$$q_0 \xrightarrow{L/l} q_1 \xrightarrow{A/a} q_2 \xrightarrow{K/k} q_3 \xrightarrow{S/s} q_4 \xrightarrow{A/a} q_5$$

- At $q_5$, if the next character is non-alphabetic (space, comma, period, end-of-text), the match is **accepted**.
- At $q_5$, if the next character is alphabetic (e.g., "Laksam"), the DFA transitions to $q_{trap}$ and the match is **rejected**.
- At any state $q_i$, a non-matching alphabetic character sends the DFA to $q_{trap}$.
- From $q_{trap}$, the DFA returns to $q_0$ only when a non-alphabetic character (word boundary) is encountered.

---

# II. Implementation Information

## 2.1 How Strings Are Read and Processed

The program reads a text file (`sample.txt`) using Python's built-in file I/O. The `read_file()` function constructs the file path relative to the script's directory using `os.path.dirname(os.path.abspath(__file__))` and reads the entire file into a single string.

The core processing follows the DFA simulation exactly:

1. The text string is iterated **one character at a time** from left to right using Python's `enumerate()` function, which provides both the index and the character.
2. For each character, the program evaluates the transition function for **every pattern** independently.
3. Each pattern maintains its own current state, tracked in a dictionary.
4. When a pattern reaches its accept state ($q_n$) and the next character is a word boundary, the match is confirmed and the starting position is recorded.
5. At the end of the text, any pattern still in its accept state is also confirmed (end-of-text counts as a boundary).

The processing loop can be summarized as:

```
for each character c at position i in the text:
    for each pattern p:
        if state[p] == ACCEPT and c is a boundary:
            record match at pending position
        state[p] = δ(state[p], c)
        if entering state 1 from BOUNDARY:
            record i as the pending start position
```

## 2.2 Overview of Programming Constructs

The program is implemented in **Python** and uses the following constructs:

| Construct | Purpose |
|---|---|
| **Functions** | `read_file()`, `is_boundary_char()`, `transition()`, `run_dfa()`, `print_results()`, `print_highlighted()` — modular design separating I/O, DFA logic, and output |
| **Dictionaries** | `state`, `pending`, `matches` — each keyed by pattern string, used to track the current DFA state, the start position of the current match attempt, and the list of confirmed match positions respectively |
| **Lists** | Store the patterns to search for and the positions of confirmed matches |
| **`enumerate()`** | Iterates over the text providing both the character index (position) and the character value |
| **String methods** | `.isalpha()` for boundary detection, `.lower()` for case-insensitive comparison |
| **ANSI escape codes** | `\033[1m` and `\033[0m` for bold text visualization in terminal output |
| **`if __name__ == "__main__"`** | Standard Python entry point guard for proper module structure |
| **`os.path` functions** | `dirname()`, `abspath()`, `join()` — for platform-independent file path construction |

---

# III. Conclusion

This project implements a DFA-based recognizer for **Language L4: Food Finder**, capable of identifying **140+ Malaysian food names** in any given text. The program faithfully simulates a finite state machine by processing exactly one character at a time from left to right, with clearly defined states (BOUNDARY, partial match, ACCEPT, and TRAP) and transition rules.

The output displays:

- The text used for demonstration
- Each pattern with its **accept/reject status**
- The **number of occurrences** and their **positions** in the text
- A **bold-highlighted visualization** of all matched food names within the text

Testing with the provided `sample.txt` (a passage about Malaysian cuisine) successfully identifies food items such as *Nasi Lemak*, *Roti Canai*, *Teh Tarik*, *Char Kway Teow*, *Laksa*, *Rendang*, *Satay*, *Ais Kacang*, *Cendol*, and many more, confirming the correctness of the DFA implementation.

---

# IV. Appendix — Full Source Code

```python
"""
CPT411 Assignment 1 – Food Finder (L4)
Deterministic Finite Automaton (DFA) that recognizes Malaysian food names
in a given text by processing one character at a time from left to right.

DFA Definition:
    Σ  = { a..z, A..Z, 0..9, and other symbols found in the sample text }
    Q  = { BOUNDARY, TRAP, 1, 2, ..., len(pattern) }
    q0 = BOUNDARY
    F  = { len(pattern) }  (accepting state, confirmed at next word boundary)

    Transitions:
        BOUNDARY + matching char   → state 1 (start matching)
        BOUNDARY + alpha non-match → TRAP
        BOUNDARY + non-alpha       → BOUNDARY
        state i  + matching char   → state i+1 (continue matching)
        state i  + non-matching alpha → TRAP
        state i  + non-alpha       → BOUNDARY (partial match broken)
        TRAP     + alpha           → TRAP (stay trapped)
        TRAP     + non-alpha       → BOUNDARY (reset at word boundary)
        ACCEPT   + non-alpha       → BOUNDARY (match confirmed)
        ACCEPT   + alpha           → TRAP (not a whole word)
"""

import os

# --- DFA State Constants ---
BOUNDARY = 0    # q0: at a word boundary (start of text or after a non-alpha character)
TRAP     = -1   # Trap state: inside a non-matching word, no valid transition out until boundary


def read_file(filename):
    """Read and return the contents of a text file in the script's directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def is_boundary_char(c):
    """Return True if character is a word boundary (non-alphabetic)."""
    return not c.isalpha()


def transition(state, char, pattern):
    """
    DFA transition function δ(state, char) → next_state.
    Processes exactly one character and returns the new state.
    """
    # Trap state: stay trapped until a boundary resets us
    if state == TRAP:
        return BOUNDARY if is_boundary_char(char) else TRAP

    # Accept state reached: confirm match only at a word boundary
    if state == len(pattern):
        return BOUNDARY if is_boundary_char(char) else TRAP

    # BOUNDARY or partial match (states 1..len-1): try to advance
    if char.lower() == pattern[state].lower():
        return state + 1       # matched next character in pattern
    elif is_boundary_char(char):
        return BOUNDARY        # non-alpha resets to boundary
    else:
        return TRAP            # wrong alpha character → trap


def run_dfa(text, patterns):
    """
    Run the DFA over the text for each pattern, processing one character
    at a time from left to right. Returns a dict mapping each pattern
    to a list of starting positions where it was found.
    """
    state   = {p: BOUNDARY for p in patterns}
    pending = {p: -1       for p in patterns}
    matches = {p: []       for p in patterns}

    for i, char in enumerate(text):
        for p in patterns:
            s = state[p]

            # If in accept state and current char is a boundary, confirm the match
            if s == len(p) and is_boundary_char(char):
                matches[p].append(pending[p])

            # Compute next state (one character at a time)
            new_state = transition(s, char, p)

            # Record where a new match attempt begins (entering state 1 from boundary)
            if new_state == 1 and s == BOUNDARY:
                pending[p] = i

            state[p] = new_state

    # End-of-text counts as a word boundary: confirm any pending accept states
    for p in patterns:
        if state[p] == len(p):
            matches[p].append(pending[p])

    return matches


def print_results(text, results):
    """Print accept/reject status, occurrence count, and positions for each pattern."""
    print("\n--- Results ---")
    for pattern, positions in results.items():
        if positions:
            print(f"Pattern '{pattern}': ACCEPTED – {len(positions)} occurrence(s) "
                  f"at position(s) {positions}")
        else:
            print(f"Pattern '{pattern}': REJECTED – 0 occurrence(s)")


def print_highlighted(text, results, patterns):
    """Visualize matches by printing the text with matched words in bold."""
    BOLD = '\033[1m'
    END  = '\033[0m'

    # Collect all match spans and sort by position
    spans = []
    for p in patterns:
        for pos in results[p]:
            spans.append((pos, len(p)))
    spans.sort()

    highlighted = ""
    prev_end = 0
    for pos, length in spans:
        if pos >= prev_end:  # skip overlapping matches
            highlighted += text[prev_end:pos]
            highlighted += f"{BOLD}{text[pos:pos + length]}{END}"
            prev_end = pos + length
    highlighted += text[prev_end:]

    print("\n--- Highlighted Text ---")
    print(highlighted)


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # List of Malaysian food patterns to recognize
    patterns = [
        # Staple foods
        "Ambuyat", "Bee Hoon", "Pulut", "Ketupat", "Kway teow", "Lemang",
        "Mi", "Nasi putih",

        # Main dishes
        "Ayam bakar", "Ayam goreng", "Ayam kecap", "Ayam percik", "Ayam tandori",
        "Asam pedas fish", "Bean Sprouts Chicken", "Chai tow kway", "Chilli crab",
        "Curry", "Fish ball", "Gulai", "Ikan Bakar", "Ikan goreng", "Kari ayam",
        "Kari kambing", "Kari kepala ikan", "Begedil", "Rendang", "Telur pindang",
        "Tempoyak ikan patin", "Otak-otak", "Oyster omelette", "Sata", "Satay",
        "Satay celup",

        # Soups
        "Sop ekor", "Sup Kambing", "Sayur Lodeh", "Yong tau foo", "Ayam pansuh",
        "Bak kut teh",

        # Breads
        "Apam", "Chapathi", "Dosai", "Kaya toast", "Murtabak", "Naan",
        "Ramly Burger", "Roti canai", "Roti Jala", "Roti John",

        # Salads
        "Acar", "Kinilaw", "Pasembur", "Popiah", "Rojak", "Ulam", "Urap",
        "Yusheng", "Yee Sang",

        # Noodle dishes
        "Pan mee", "Char kway teow", "Curry Mee", "Duck soup noodles",
        "Hokkien mee", "Laksa", "Laksa Sarawak", "Lor mee", "Maggi goreng",
        "Mee Bandung Muar", "Mee goreng", "Mee hailam", "Mee Kolok", "Mee pok",
        "Mee rebus", "Mee siam", "Mee sup", "Mihun sup", "Soto", "Wonton noodles",

        # Rice dishes
        "Banana Leaf Rice", "Briyani", "Bubur Ashura", "Bubur ayam",
        "Bubur Pedas", "Claypot chicken rice", "Hainanese Chicken Rice",
        "Nasi Ambeng", "Economy rice", "Nasi Dagang", "Nasi daging",
        "Nasi Goreng", "Nasi goreng pattaya", "Nasi Hujan Panas", "Nasi Itik",
        "Nasi Kandar", "Nasi kebuli", "Nasi kerabu", "Nasi Kuning", "Nasi Lemak",
        "Nasi minyak", "Nasi paprik", "Nasi Tomato", "Nasi Tumpang", "Nasi ulam",

        # Snacks
        "Keropok", "Kerepek", "Jemput-jemput", "Cokodok", "Cucur", "Curry puff",
        "Amplang", "Rempeyek", "Mee Siput Muar", "Keropok lekor", "Pisang goreng",
        "Akok", "Kuih peria", "Kuih kosui",

        # Preserved meat
        "Bakkwa", "Belutak", "Char siu", "Chinese sausage", "Dendeng", "Pekasam",
        "Serunding", "Sinalau Bakas",

        # Desserts
        "Ais kacang", "Agar Agar", "Cendol", "Dadih", "Dodol",
        "Bubur kacang hijau", "Bubur pulut hitam", "Bubur cha cha",
        "Mango sticky rice", "Durian sticky rice", "Roti tissue",
        "Puding Diraja", "Putu mayam", "Tapai",

        # Spreads
        "Kacang Coklat", "Kaya",

        # Condiments and sauces
        "Belacan", "Budu", "Cincalok", "Kerisik", "Sweet soy sauce",
        "Kicap Masin", "Otak Udang", "Sambal", "Sos Tiram", "Tauco",
        "Tempoyak", "Tuhau",

        # Cakes and pastries
        "Batik cake", "Kek Lapis Sarawak", "Pandan cake", "Bahulu",
        "Malay sponge cake",

        # Drinks
        "Bandung", "Ipoh white coffee", "Janda pulang", "Coconut water",
        "Susu Kacang Soya", "Teh See", "Teh halia", "Teh krisantimum",
        "Teh tarik", "Teh C Peng Special", "Tenom coffee", "Milo Dinosaur",
        "Tuak"
    ]

    # Read text and run DFA
    text = read_file("sample.txt")

    print("--- Text Used for Demo ---")
    print(text)

    results = run_dfa(text, patterns)

    print_results(text, results)
    print_highlighted(text, results, patterns)
```
