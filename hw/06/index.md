# HW6 - Recommender systems

Solution of homework 6.

## Task (assignment)

- Use the existing [MovieLens dataset](https://grouplens.org/datasets/movielens/)
    - use the dataset version recommended for education and development
    - Focus on the ratings.csv and movies.csv dataset partitions
- Implement content-based recommender system
    - Represent each movie (item) as a set of genres
        - use movies.csv
        - Toy Story (1995), genres: Adventure, Animation, Children, Comedy, Fantasy
        - represent this info as vector
    - Build user profiles consisting of genres instead of movies, example:
        - use ratings.csv and movies.csv
        - user-id: Action, Adventure, Animation, Comedy, Fantasy, Film-Noir, Horror
    - 0 if rating is <2.5, 1 if rating is >=2.5
    - for users which rated movies with same genre, add +1 to the genre field (if rating >= 2.5)
        - Compute similarity between the user profile vector and each item vector
        - Recommend top-N most similar items
    - previously not rated by the user
        - Implement hybrid recommender system
            - combine the results from the CF implementation from the tutorial and the content based recsys from this task
            - normalize the results from the CF and content based so that they are in the interval [0, 1]
            - aggregate the results using weighting scheme
            - e.g. 0.3 for the content based, 0.7 for the collaborative filtering

Weighting example (with 3 items) for a user with 0.3 for content based and 0.7 for collaborative filtering:

- results from content based
    - item-1: 0.8 (rank 1)
    - item-2: 0.7 (rank 2)
    - item-3: 0.5 (rank 3)
- results from collaborative filtering
    - item-1: 0.4 (rank 3)
    - item-2: 0.5 (rank 2)
    - item-3: 0.7 (rank 1)
- results from hybrid
    - item-1: 0.8 x 0.3 + 0.4 x 0.7 = 0.52 (rank 3)
    - item-2: 0.7 x 0.3 + 0.5 x 0.7 = 0.56 (rank 2)
    - item-3: 0.5 x 0.3 + 0.7 x 0.7 = 0.64 (rank 1)
- Evaluate your system
    - split your dataset in two parts
        - awk ‚NR % 2 != 0‘ ratings.csv > new-ratings.csv
        - != for training part, == for testing part
        - training: one part to compute similarities and generate recommendations
        - testing: other part to evaluate the recommendations
    - Evaluation metrics
        - compute Precision, Recall, F-measure
        - you can re-use code from homework 2
    - Evaluate the:
        - content based implementation
        - collaborative filtering implementation (from the tutorial)
        - hybrid approach
            - try out at least three different weghting scheme
            - e.g. 0.3+0.7, 0.5+0.5, 0.7+0.3

## Solution

By agreement, I will use my implementation of the testing algorithm for recommender 
systems to test the content-based recommendation (attribute item-knn) for this task. 
Collaborative filtering algorithms (user-knn and item-knn) are also used in the test library. 
These algorithms serve primarily as a reference to the comparison of referrals 
against attributes. The framework will be supplemented by testing a hybrid approach 
for the combination of algorithms as well as the precision and F-measure metrics. 
The algorithms will not be taught on the tutorial data but will use Movielens1M to test, 
and then a full, uncut, Movielens20M dataset.

The main function of the framework is the possibility to test the locality-sensitive hashing for attribute
item-knn on model with many attributes (long description, category, price) and datatypes, 
where it may yield relatively good results.

### Algorithms
There I will describe the state of the art of the algorithms used in the system. 
All these algorithm are based on computing similarity between the vectors.

#### Content-based item-knn
I have implemented a content-based algorithm by creating vectors from all 
available attributes first. You can process numbers into bins for example. 
The timestamps into different intervals. The text is processed by tokenization 
and tf-idf is counted. And then also sets. The set will also be used by Movielens (genre).

After tokenization, I have vectors on which to calculate similarity. 
I will always return the most similar to each item. 
These similar is the recommendation for the item. 
This is a bit different from user-based knn.

Below is a sample of the closest neighbors looking for implementation:
```python
def get_k_nearest(self, item_id, query_item_vector, k):
    if item_id and item_id in self.cache and len(self.cache[item_id]) >= k:
        return self.cache[item_id][:k]
    else:
        nearest_items = []
        query_sum = count_sum_product(query_item_vector)
        for item in possible_items:
            if item_id and item == item_id:
                continue
            nearest_items.append([
                item,
                self.cosine_similarity_fmid(
                    query_item_vector,
                    query_sum,
                    self.data.get_item_vector(item),
                    self.data.get_item_sum(item)
                )
            ])
        nearest_items.sort(key=lambda x: (x[1]), reverse=True)
        if item_id and k > len(self.cache[item_id]):
            self.cache[item_id] = nearest_items
        return nearest_items[:k]
        
def cosine_similarity_fmid(user_a, sum_a, user_b, sum_b):
    # one sqrt -> both sum are positive
    return AttributeItemKnn.dot_sparse_vectors(user_a, user_b) / math.sqrt(sum_a * sum_b)
```


#### Interaction user-knn
User knn uses the interaction similarities of individual users. 
After finding the most similar users, a recommendation is generated. 
In this case, the values are calculated for items with which the 
querying user has not met and the value calculated by the value of 
the user's similarity dot how much the item liked the user. 
N items with the highest value are recommended.

Below is an example of generating recommendations from the closest users. 
Get_k_nearest is the same as the item-knn attribute:
```python
def get_n_recommendation(self, query_vector, k, n):
    items_and_weight = {}
    for u in self.get_k_nearest(query_vector, k):
        items = self.data.get_row(u[0])
        weight_of_user = u[1]
        for item in items:
            if item in query_vector:
                continue
            if item not in items_and_weight:
                items_and_weight[item] = float(items[item]) * weight_of_user
            else:
                items_and_weight[item] += float(items[item]) * weight_of_user
    recommendation = [[k, items_and_weight[k]] for k in items_and_weight]
    recommendation.sort(key=lambda x: (x[1]), reverse=True)
    return recommendation[:n]
```

#### Interaction item-knn
Interaction item-knn is the same as user-knn with the transpose interaction (rating) matrix.
The difference is only the way how to recommend. The similar items are computed for each item in the user vector.
Then the resulting recommendation is created, 
so it is for each item sum over all recommendations weighted by 
how much the item liked the user. 
The recommendation is then n items with the highest value.

### Testing recommendation
There I will describe how I generate and test the recommendation. 
I will test the top-5 recommendation. From test set of users for each 
I will remove one item from vector and generate a recommendation. 
If the remove item is in recommended items, it is successful and conversely.

#### Content-based item-knn and interaction item-knn
For these algorithms, testing is the same; others are only vectors for items.  
Here, two methods can be used, namely the method of generating the 
recommendations mentioned above, where the nearest neighbors are generated for each item. 
The second method is described in the task assignment and that it 
is possible to create one item from the user items (super-item). 
Then find the similar to this. 
So, for example, a list of genres. I'll test both implementations.

#### Interaction user-knn
I described this recommendation above.

#### Hybrid approach
There I will generate the list of recommendation for each model in combination (CF and content-based)
The size of recommendation will be higher than n (5) I will try all possible for example.
The I will normalize similarities and using weights of algorithm do weighing of the recommendation.
On the result, I will measure the metrics.

### Results
I will plot graphs with the recall vs. coverage curve. 
Coverage is the percentage of how many different items were recommended by 
the system from the whole catalog of items. This criterion may be necessary in many cases. 
The referral system won't be able to recommend all items, 
but it is also not advisable to recommend only a few bestsellers. 
For accurate testing, it is necessary to choose a fixed size of 
the test set because the absolute value is dependent on it. 
I select the size of the test set 300 for MovieLens1M and 1500 for MovieLens20M.
#### Content-based item-knn
...
#### Interaction item-knn
...
#### Interaction user-knn
...
#### Hybrid approach
...

### Issues during design/implementation
There were no issues during implementation.
### Ideas for extensions/improvements/future work
In the tutorial or task, I may have missed a reference to classic 
and commonly used referrals when using item-knn algorithms, 
both content-based and rating-based. When in a task we build a 
profile for a user, for which we are looking for the closest items. 
You can also use the approach where the nearest items are searched 
for each item with which the user interacted, and the results then merged appropriately. 
This approach will usually lead to better results. #TODO: results 
