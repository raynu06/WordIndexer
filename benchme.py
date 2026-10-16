import os
import time
import random
import matplotlib.pyplot as plt
from indexer import TrieIndex, BSTIndex, DictIndex, parse_and_index

def benchmark_all():
    os.makedirs("graphs", exist_ok=True)
    dataset_counts = [1000, 5000, 10000, 50000, 100000, 500000]
    
    trie_build, bst_build, dict_build = [], [], []
    trie_search, bst_search, dict_search = [], [], []
    trie_print, bst_print, dict_print = [], [], []

    for count in dataset_counts:
        filepath = os.path.join("data", f"input_{count}.txt")
        if not os.path.exists(filepath):
            print(f"Skipping {filepath} (run generate_data.py first)")
            continue
            
        print(f"\n--- Benchmarking Dataset: {count} distinct words ---")

        # 1. Trie Benchmark
        trie = TrieIndex()
        t1 = time.perf_counter()
        parse_and_index(filepath, trie)
        trie_build.append(time.perf_counter() - t1)

        words = [item[0] for item in trie.get_lexicographical_index()]
        queries = random.choices(words, k=100000)

        t1 = time.perf_counter()
        for w in queries: trie.search(w)
        trie_search.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        trie.get_lexicographical_index()
        trie_print.append(time.perf_counter() - t1)

        # 2. BST Benchmark
        bst = BSTIndex()
        t1 = time.perf_counter()
        parse_and_index(filepath, bst)
        bst_build.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        for w in queries: bst.search(w)
        bst_search.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        bst.get_lexicographical_index()
        bst_print.append(time.perf_counter() - t1)

        # 3. Dict Benchmark
        dct = DictIndex()
        t1 = time.perf_counter()
        parse_and_index(filepath, dct)
        dict_build.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        for w in queries: dct.search(w)
        dict_search.append(time.perf_counter() - t1)

        t1 = time.perf_counter()
        dct.get_lexicographical_index()
        dict_print.append(time.perf_counter() - t1)

    # Plotting results
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(dataset_counts[:len(trie_build)], trie_build, label='Trie', marker='o')
    plt.plot(dataset_counts[:len(bst_build)], bst_build, label='BST', marker='s')
    plt.plot(dataset_counts[:len(dict_build)], dict_build, label='Dict', marker='^')
    plt.title('Construction Time')
    plt.xlabel('Distinct Words')
    plt.ylabel('Seconds')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(dataset_counts[:len(trie_search)], trie_search, label='Trie', marker='o')
    plt.plot(dataset_counts[:len(bst_search)], bst_search, label='BST', marker='s')
    plt.plot(dataset_counts[:len(dict_search)], dict_search, label='Dict', marker='^')
    plt.title('Search Time (100k queries)')
    plt.xlabel('Distinct Words')
    plt.ylabel('Seconds')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(dataset_counts[:len(trie_print)], trie_print, label='Trie', marker='o')
    plt.plot(dataset_counts[:len(bst_print)], bst_print, label='BST', marker='s')
    plt.plot(dataset_counts[:len(dict_print)], dict_print, label='Dict', marker='^')
    plt.title('Retrieval / Print Time')
    plt.xlabel('Distinct Words')
    plt.ylabel('Seconds')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('graphs/performance_comparison.png')
    print("\nBenchmark complete! Graphs saved to graphs/performance_comparison.png")

if __name__ == "__main__":
    benchmark_all()