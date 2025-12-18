# test_visualize.py（测试用）
from loader import load_text
from splitter import split_words
from hash_chaining import HashTableChaining
from sorter import quick_sort
from visualize import draw_top_words

text = load_text("data/input.txt")
words = split_words(text)

ht = HashTableChaining()
ht.build(words)

nodes = ht.get_all_nodes()
sorted_nodes = quick_sort(nodes)

draw_top_words(sorted_nodes, top_n=10, save_path="output/freq_chart.png")
