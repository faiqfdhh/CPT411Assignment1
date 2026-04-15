import os

def read_file(filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))        
    filepath = os.path.join(script_directory, filename)
    
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def transition(state, char, word):
    if state == -1:
        return -1
    if state == len(word):
        return state
    if char.lower() == word[state].lower():
        return state + 1
    else:
        return -1

def run_dfa(text, list_of_words):
    state = {word: 0 for word in list_of_words}
    matches = {word: [] for word in list_of_words}
    
    for i, char in enumerate(text):
        for word in list_of_words:
            current_state = state[word]
            new_state = transition(current_state, char, word)
            
            if new_state == len(word):
                start_pos = i - len(word) + 1
                matches[word].append(start_pos)
                state[word] = 0

            elif new_state == -1:
                if char.lower() == word[0].lower():
                    state[word] = 1
                else:
                    state[word] = 0
            else:
                state[word] = new_state
                
    return matches

def print_bolded_text(original_text, results, words):
    BOLD = '\033[1m'
    END = '\033[0m'
    
    highlighted_text = original_text
    
    for word in words:
        if len(results[word]) > 0: 
            highlighted_text = highlighted_text.replace(word, f"{BOLD}{word}{END}")
            highlighted_text = highlighted_text.replace(word.capitalize(), f"{BOLD}{word.capitalize()}{END}")
            
    print("\n--- Visualized Text ---")
    print(highlighted_text)


# Read from a .txt file (Ensure 'sample.txt' exists in the same directory)
text = read_file("sample.txt")
list_of_words = [
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

results = run_dfa(text, list_of_words)

print("--- Summary ---")
for word, positions in results.items():
    # Only print if the positions list is not empty
    if positions: 
        print(f"Pattern '{word}': {len(positions)} occurrence(s) found at indices {positions}")

print_bolded_text(text, results, list_of_words)