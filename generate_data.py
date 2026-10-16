import os
import random
import string

def generate_random_word(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def create_dataset(filename, num_distinct_words, total_words=1000000):
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    
    vocabulary = [generate_random_word(random.randint(3, 8)) for _ in range(num_distinct_words)]
    
    print(f"Generating {filename} with {num_distinct_words} distinct words...")
    words_per_line = 10
    total_lines = total_words // words_per_line

    with open(filepath, 'w', encoding='ascii') as f:
        for line_num in range(1, total_lines + 1):
            line_words = random.choices(vocabulary, k=words_per_line)
            f.write(" ".join(line_words) + ".\n")
    print(f"Saved: {filepath}")

if __name__ == "__main__":
    # Generating datasets matching your assignment requirements
    counts = [1000, 5000, 10000, 50000, 100000, 500000]
    for count in counts:
        create_dataset(f"input_{count}.txt", count, total_words=1000000)