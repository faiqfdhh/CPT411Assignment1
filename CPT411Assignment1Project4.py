import os
from datetime import datetime

# --- DFA State Constants ---
BOUNDARY = 0    # q0: at a word boundary (start of text or after a non-alpha character)
TRAP     = -1   # Trap state: inside a non-matching word, no valid transition out until boundary


def read_file(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def is_boundary_char(c):
    return not c.isalpha()


def transition(state, char, pattern):

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
  
    state   = {p: BOUNDARY for p in patterns}
    pending = {p: -1       for p in patterns}   # start position of current match attempt
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


def format_results(results):
    lines = ["--- Results ---"]
    found_any = False

    for pattern, positions in results.items():
        if positions:
            found_any = True
            lines.append(
                f"Pattern '{pattern}': ACCEPTED - {len(positions)} occurrence(s) at position(s) {positions}"
            )

    if not found_any:
        lines.append("No matching patterns found.")

    return "\n".join(lines)


def to_plaintext_bold(text):
    bold_chars = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            bold_chars.append(chr(0x1D5D4 + ord(ch) - ord('A')))
        elif 'a' <= ch <= 'z':
            bold_chars.append(chr(0x1D5EE + ord(ch) - ord('a')))
        elif '0' <= ch <= '9':
            bold_chars.append(chr(0x1D7EC + ord(ch) - ord('0')))
        else:
            bold_chars.append(ch)
    return "".join(bold_chars)


def format_highlighted(text, results, patterns):
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
            highlighted += to_plaintext_bold(text[pos:pos + length])
            prev_end = pos + length
    highlighted += text[prev_end:]

    return highlighted


def write_output_file(text, results, patterns):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output{timestamp}.txt"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, filename)

    sections = [
        "--- Text Used for Demo ---",
        text,
        "",
        format_results(results),
        "",
        "--- Highlighted Text ---",
        format_highlighted(text, results, patterns),
        "",
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sections))

    return output_path


def open_output_file(filepath):
    try:
        os.startfile(filepath)
    except Exception as e:
        print(f"Could not auto-open file: {e}")


# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # List of Malaysian food patterns to recognize
    patterns = [
        # Staple foods
        "Ambuyat", "Bee Hoon", "Pulut", "Ketupat", "Kway teow", "Lemang", "Mi", "Nasi putih",

        # Main dishes
        "Ayam bakar", "Ayam goreng", "Ayam kecap", "Ayam percik", "Ayam tandori", "Asam pedas fish",
        "Bean Sprouts Chicken", "Chai tow kway", "Chilli crab", "Curry", "Fish ball", "Gulai",
        "Ikan Bakar", "Ikan goreng", "Kari ayam", "Kari kambing", "Kari kepala ikan", "Begedil",
        "Rendang", "Telur pindang", "Tempoyak ikan patin", "Otak-otak", "Oyster omelette", "Sata",
        "Satay", "Satay celup",

        # Soups
        "Sop ekor", "Sup Kambing", "Sayur Lodeh", "Yong tau foo", "Ayam pansuh", "Bak kut teh",

        # Breads
        "Apam", "Chapathi", "Dosai", "Kaya toast", "Murtabak", "Naan", "Ramly Burger", "Roti canai",
        "Roti Jala", "Roti John",

        # Salads
        "Acar", "Kinilaw", "Pasembur", "Popiah", "Rojak", "Ulam", "Urap", "Yusheng", "Yee Sang",

        # Noodle dishes
        "Pan mee", "Char kway teow", "Curry Mee", "Duck soup noodles", "Hokkien mee", "Laksa",
        "Laksa Sarawak", "Lor mee", "Maggi goreng", "Mee Bandung Muar", "Mee goreng", "Mee hailam",
        "Mee Kolok", "Mee pok", "Mee rebus", "Mee siam", "Mee sup", "Mihun sup", "Soto", "Wonton noodles",

        # Rice dishes
        "Banana Leaf Rice", "Briyani", "Bubur Ashura", "Bubur ayam", "Bubur Pedas", "Claypot chicken rice",
        "Hainanese Chicken Rice", "Nasi Ambeng", "Economy rice", "Nasi Dagang", "Nasi daging",
        "Nasi Goreng", "Nasi goreng pattaya", "Nasi Hujan Panas", "Nasi Itik", "Nasi Kandar",
        "Nasi kebuli", "Nasi kerabu", "Nasi Kuning", "Nasi Lemak", "Nasi minyak", "Nasi paprik",
        "Nasi Tomato", "Nasi Tumpang", "Nasi ulam",

        # Snacks
        "Keropok", "Kerepek", "Jemput-jemput", "Cokodok", "Cucur", "Curry puff", "Amplang", "Rempeyek",
        "Mee Siput Muar", "Keropok lekor", "Pisang goreng", "Akok", "Kuih peria", "Kuih kosui",

        # Preserved meat
        "Bakkwa", "Belutak", "Char siu", "Chinese sausage", "Dendeng", "Pekasam", "Serunding", "Sinalau Bakas",

        # Desserts
        "Ais kacang", "Agar Agar", "Cendol", "Dadih", "Dodol", "Bubur kacang hijau", "Bubur pulut hitam",
        "Bubur cha cha", "Mango sticky rice", "Durian sticky rice", "Roti tissue", "Puding Diraja",
        "Putu mayam", "Tapai",

        # Spreads
        "Kacang Coklat", "Kaya",

        # Condiments and sauces
        "Belacan", "Budu", "Cincalok", "Kerisik", "Sweet soy sauce", "Kicap Masin", "Otak Udang",
        "Sambal", "Sos Tiram", "Tauco", "Tempoyak", "Tuhau",

        # Cakes and pastries
        "Batik cake", "Kek Lapis Sarawak", "Pandan cake", "Bahulu", "Malay sponge cake",

        # Drinks
        "Bandung", "Ipoh white coffee", "Janda pulang", "Coconut water", "Susu Kacang Soya", "Teh See",
        "Teh halia", "Teh krisantimum", "Teh tarik", "Teh C Peng Special", "Tenom coffee", "Milo Dinosaur", "Tuak"
    ]

    # Read text and run DFA
    text = read_file("sample.txt")

    results = run_dfa(text, patterns)

    output_path = write_output_file(text, results, patterns)
    print(f"Output written to: {output_path}")
    open_output_file(output_path)
