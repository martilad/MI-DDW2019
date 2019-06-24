import nltk
import networkx

# input text
text = None
with open('text.txt', 'r') as f:
    text = f.read()

# process text and convert to a graph
sentences = [[t for t in nltk.word_tokenize(sentence)] for sentence in nltk.sent_tokenize(text)]
G=nx.Graph()
# G.add_node(...
# G.add_edge(...

# ...

# visualise
plt.figure(figsize=(20,10))
pos = graphviz_layout(G, prog="fdp")
nx.draw(G, pos,
        labels={v:str(v) for v in G},
        cmap = plt.get_cmap("bwr"),
        node_color=[G.degree(v) for v in G],
        font_size=12
       )
plt.show()

# write to GEXF
nx.write_gexf(G, "export.gexf")
