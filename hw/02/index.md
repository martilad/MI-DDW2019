# HW2 - Indexing & Document Retrieval
Solution of homework 2.

## Task (assignment)

* Download an existing IR dataset - [Cranfield collection](http://ir.dcs.gla.ac.uk/resources/test_collections/cran/)
    * Or you can use already preprocessed data cranfield.zip 
    (d-documents, q-queries, r-relevances (a set of relevant document ids for each query id))
* Represent each document and query using the Vector Space Model with all following weightings:
    * Use Binary representation
    * Use pure Term Frequency
    * Use TF-IDF
* Compute relevance scores for each combination of query, document
    * Use Euclidean distance
    * Use Cosine similarity measure
* Evaluate quality and difference of both scores and different weighting schemas
    * Compute Precision, Recall, F-measure (you can limit to top N relevant documents for each query)

## Solution

This task I processed in Jupyter notebook (src/VectorModel.ipyb) and python 3.7.

### Weighting schemas
In addition to the entered weighing schemes (tf-idf, tf, binary), 
I added one more, raw count (rc), which is the first step to calculate the tf.

* __raw count__ - This is just the count for a given term in a document. 
    This scheme should, therefore, favor broad documents and be manifested primarily at Euclidean distance.
* __binary__ - This schema only numbers greater than 0 will replace 1.
    For this scheme, Euclidean distance could already be more successful, 
    but it could still be too advantageous for long documents that contain a lot of terms.
* __tf__ - The tf scheme is the number of terms normalized by the length of the document. 
      In this case, both Cosin's similarity and Euclidean distance could already be applicable.
* __tf-idf__ - Tf-idf is successful metric and used in information retrieval. 
    It consists of two components, namely tf and then idf, 
    which is determining the importance of a word in a collection of documents. 
    However, this weighting schema has a problem in processing large amounts of data in real time, 
    where it is very difficult to implement or cannot be implemented 100% real-time.

### Evaluation
In vector space, the similarity metric or distance comparison vector must be defined. 
In this task, I tested two metrics:

* __Euclidean distance__ - Known metric, which is however sensitive to vector component sizes.

* __Cosine similarity__ - The angle-based metric of the vectors by which the similarity is determined.
    
To evaluate the success I will measure precision, recall and f1-score (F-meansure).

* __precision__ - true positives / (true positives + false positive)

* __recall__  - true positives / (true positives + false negative)

* __f1__ - 2 * true positives / (2 * true positives + false positive +  false negative)

### Implementation
For implementation, I used the library sklearn, 
where there are many methods and metrics implemented, 
and it was not necessary to deal with their implementation.

First, I retrieve data from files and create individual vector models with a given weight. 
Then, for each document and each weighing, 
I calculate the cosine similarity or Euclidean distance and save it separately in CVS files.

Then I evaluate for each combination of individual metrics and schemes. 
I implemented the ratings as average values across all query documents.

For the purpose, I have introduced graphs for tf-idf and both metrics. 
Iterated over N (the number of relevant ones that you select) after 10 and plotted precision, recall, 
and f1-score. On this plot, you can see the behavior of these success metrics beautifully.

### Results
Computed relevance score for each combination 
and each query document are in folder results named first with weighting schema and then with metric. 

Evaluation of quality on different metric and weighting schema I provide in the notebook.
In this case, it was very difficult to determine N. 
So I describe it in [Issues during design/implementation](#issues-during-design-implementation)

Bellow are the result for dynamic N:

##### tf-idf and euclidean distance
* Average recall: 0.49879757943258907
* Average precision: 0.12475095785440622
* Average F-meansure: 0.18959857704755778
##### tf-idf and cosine similarity
* Average recall: 0.5065055813072575
* Average precision: 0.1265900383141763
* Average F-meansure: 0.19248219777713485
##### tf and euclidean distance
* Average recall: 0.3579317800635903
* Average precision: 0.09241379310344836
* Average F-meansure: 0.13942847089217847
##### tf and cosine similarity
* Average recall: 0.44647888863288687
* Average precision: 0.1121839080459771
* Average F-meansure: 0.17029899219588607
##### raw count of terms and euclidean distance
* Average recall: 0.04004874648552809
* Average precision: 0.009501915708812264
* Average F-meansure: 0.014438151004604029
##### raw count of terms and cosine similarity
* Average recall: 0.44499740715140534
* Average precision: 0.11203065134099625
* Average F-meansure: 0.17002121441810827
##### binary representation and euclidean distance
* Average recall: 0.04727056787401613
* Average precision: 0.011647509578544057
* Average F-meansure: 0.01776157682613699
##### binary representation and cosine similarity
* Average recall: 0.4550348499555149
* Average precision: 0.11157088122605374
* Average F-meansure: 0.17061639258335246

The results show that for tf-idf there is almost no difference between cosine similarity and Euclidean distance. 
This, it can theoretically be said that the scheme is very robust, 
but this could be expected from its definition. But it is also not ideal for any use just from counting idf.

In other metrics, cosine resemblance to Euclidean distance is already dominating.

The most significant difference is seen in non-standardized weighing schemes (raw count and binary), 
which confirmed expectations.

From the results I was very pleasantly surprised by the success of 
the binary representation of the vector model using cosine similarity, 
the result is not bad at all considering the simplicity of this model.

### Issues during design/implementation

The choice of N will, in no small extent, also affect the resulting metrics. 
For this reason, a graph is made at the end of the work, depending on the selected N. 
Where it can be seen that 100% recall is easy to get, 
I only return all the results, but also the accuracy decreases. For one result, 
the expected accuracy will jump, but the minimum recall.

The problem with this data is that the attached number of relevant documents to each query are not always same, 
so it would be beneficial to know the domain and set a threshold for that metric. 
If I always returned the same count of relevant, the score for some can be biased.

In the end, I choose the variables N, which I determine by the number of relevant documents provided.


