# HW4 - Social Network Analysis
Solution of homework 4.

## Task (assignment)
* Use an existing [Movie dataset](https://archive.ics.uci.edu/ml/datasets/Movie)
    * Focus on „casts“ - data that provide information about actors in movies
    * You can also use already converted data to csv from [https://github.com/cernoch/movies](https://github.com/cernoch/movies)
* Convert „casts“ data to a graph
    * Create a node for each actor
    * Create an edge if two actors appeared in the same movie
* Perform Social Network Analysis
    * Compute general statistics
    * Identify key players using centrality measures
    * Identify clusters/communities in graph
    * Compute „Kevin Bacon“ number for each actor with selected key player
    * Visualise important aspects of the analysis

## Solution

The entire implementation, including comments, is provided to the Jupyter notebook in `/src/SocialNetworkAnalysis.ipynb`. The resulting graph in \*.gexf format and visualizations are in the result folder.


### Issues during design/implementation

During the implementation I encountered problems only during visualization. The first was insufficient power to display the entire graph and then to select a suitable subset so that I wouldn't cut too much information that I would have picked up.

### Vizualization

For the first visualization I chose 2000 nodes randomly. The visualization shows actors who play in one movie and always make a component.

On other pictures I have always taken into the visualization only films with a specific number of actors, which is also listed in the file name w[number].png.

#### Random graph

<img src="04/results/random.png" width="1400">

#### 3 actors

<img src="04/results/w3.png" width="1400">

#### 18 actors

<img src="04/results/w18.png" width="1400">

#### 22 actors

<img src="04/results/w22.png" width="1400">