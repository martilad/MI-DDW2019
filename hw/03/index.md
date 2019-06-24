# HW3 - Text Mininig
Solution of homework 3.

## Task (assignment)

* Find any suitable textual data for processing which will contain at least 500 sentences.
	* you can manually collect texts from BBC/CNN/New York Times, or
	* use the crawler from the first homework/tutorial and extend it to crawl particular website and collect content for this task, or
	* use any other suitable texts (e.g. OpenData speech datasets)
* Perform following NLP tasks
	* POS tagging
	* NER with entity classification (using nltk.ne_chunk)
	* NER with custom patterns
		* e.g. every match of: adjective (optional) and proper noun (singular/plural) is matched as the entity
		* see slides 31 or 38 from lecture 4 for some NLTK examples using RegexpParser or custom NER
* Implement your custom entity classification
	* For each detected entity (using both nltk.ne_chunk and custom patterns)
		* Try to find a page in the Wikipedia
		* Extract the first sentence from the summary
		* Detect category from the sentence as a noun phrase
			* Example:
				* for „Wikipedia“ entity the first sentence is „Wikipedia (/ˌwɪkᵻˈpiːdiə/ or /ˌwɪkiˈpiːdiə/ WIK-i-PEE-dee-ə) is a free online encyclopedia that aims to allow anyone to edit articles.“
				* you can detect pattern „…​ is/VBZ a/DT free/JJ online/NN encyclopedia/NN …​“
				* the output can be „Wikipedia“: „free online encyklopedia“
		* For unknown entities assign default category e.g. „Thing“


## Solution

This task I processed in Jupyter notebook (src/textMining.ipyb) and python 3.7.

### Data description
As data for this task, I decided to download BBC news. I used the first 15 current news from March 28, 2019, 16:00.
The news is from different industries and genres, so that their vocabulary is as high as possible.
Messages are stored in individual text files in the data folder.

### Main results
There I will list some main result from each part of processing (POS tagging, NER based on ne_chunk, my own NER, entity classification (Wikipedia))

 * Number of words in dataset:  15267
 * Number of sentences in dataset:  619

#### POS tagging

There is a lot of tag of words, much more than word classes, so I will only list the most exciting tags. Top-5 for each I was the list in the notebook with implementation.

Some words that surprised me in tags I highlighted in italics.

* NN:
  * *hydrogen* - 32
  * deal - 29
  * time - 23
  * electricity - 21
  * manager - 20
* NNP:
  * *United* - 83
  * Solskjaer - 68
  * ’ - 39
  * *Mourinho* - 28
  * *League* - 25
* JJ:
  * first - 36
  * last - 17
  * new - 15
  * final - 14
* NNS:
  * people - 29
  * islands - 22
  * years - 18
  * villages - 12
  * results - 12
* NNPS:
  * Orcadians - 4
  * Commons - 3
* VBG:
  * including - 15
  * according - 11
  * winning - 7
* JJR:
  * more - 18
  * cheaper - 3
  * less - 3
* JJS:
  * most - 9
  * least - 6
  * largest - 4
  * best - 2
  * highest - 2

#### NER based on ne_chunk

There I list the top entity from nltk.ne_chunk.

* GPE:
  * Shapinsay - 60
  *  Orkney - 60
  *  Scottish - 30
  *  Stromness - 30
  *  Scotland - 30
* PERSON:
  * Orkney - 150
  *  Bews - 45
  *  Lidderdale - 30
  * Stockan - 15
  * Clipsham - 15
* ORGANIZATION:
  * EMEC - 75
  * UK - 60
  * IMO - 30
  * CCS - 30
  * Orcadians - 30
* LOCATION:
  * North Sea - 15
  * Scotland - 15

#### My own patterns

In my patterns I select

* NOUNS: {<N.\*>{2,}}\* - two or more nouns
* NOUN WITH ADJECTIVE: {\<DT>?<JJ\*><NN|NNS>} {<DT|PP\$>?\<JJ>\<NN>} - a noun with the adjective and possible too with predeterminer or determiner
* PROPER NOUN: {\<NNP*>+} - proper nouns

Bellow list the most common.

* PROPER NOUN:
  * United - 51
  * Solskjaer - 43
  * Mourinho - 23
  * Huawei - 15
  * MPs - 13
  * Dumbo - 11
  * UK - 11
  * Lloyd - 10
  * Ferguson - 10
  * Cardiff - 10
* NOUNS:
  * Old Trafford - 11
  * Champions League - 9
  * Premier League - 8
  * Manchester United - 8
  * home draw - 6
  * Mrs May - 6
  * Ole Gunnar Solskjaer - 5
  * Orkney ’ - 4
  * % possession - 4
  * Louis van Gaal - 4
* NOUN WITH ADJECTIVE:
  * last year - 7
  * the first time - 7
  * clean energy - 6
  * ’ t - 5
  * fossil fuels - 4
  * the first leg - 4
  * the 21st manager - 3
  * final game - 3
  * young players - 3
  * surplus electricity - 2

#### Entity classification using Wikipedia

Below I mentioned the most common entities that were determined by the nltk.ne_chunked. Further below, I also mentioned the results of the most frequent entities selected by my pattern. Entities were selected according to the first sentence of Wikipedia.

* Orkney
  * Description: archipelago
  * Entity: PERSON
  * Number in text: 150
* EMEC
  * Description: UKAS
  * Entity: ORGANIZATION
  * Number in text: 75
* UK
  * Description: sovereign country
  * Entity: ORGANIZATION
  * Number in text: 60
* Shapinsay
  * Description: eighth largest island
  * Entity: GPE
  * Number in text: 60
* Orkney
  * Description: archipelago
  * Entity: GPE
  * Number in text: 60
* Bews
  * Description: inherent limitations
  * Entity: PERSON
  * Number in text: 45
* Orcadians
  * Description: people
  * Entity: ORGANIZATION
  * Number in text: 30
* Orkney
  * Description: archipelago
  * Entity: ORGANIZATION
  * Number in text: 30
* Stromness
  * Description: second-most populous town
  * Entity: GPE
  * Number in text: 30
* Scotland
  * Description: country
  * Entity: GPE
  * Number in text: 30

There are entity from my pattern list in wikipedia.

* Solskjaer
  * Description: Norwegian football manager
  * Entity: PROPER NOUN
  * Number in text: 47
* Mourinho
  * Description: Portuguese professional football coach
  * Entity: PROPER NOUN
  * Number in text: 23
* hydrogen
  * Description: chemical element
  * Entity: PROPER NOUN
  * Number in text: 21
* Huawei
  * Description: Chinese multinational telecommunications equipment
  * Entity: PROPER NOUN
  * Number in text: 15
* job
  * Description: person
  * Entity: PROPER NOUN
  * Number in text: 14
* %
  * Description: symbol
  * Entity: PROPER NOUN
  * Number in text: 13
* way
  * Description: eighth studio album
  * Entity: PROPER NOUN
  * Number in text: 12
* Old Trafford
  * Description: football stadium
  * Entity: NOUNS
  * Number in text: 11
* Dumbo
  * Description: mouse
  * Entity: PROPER NOUN
  * Number in text: 11
* UK
  * Description: sovereign country
  * Entity: PROPER NOUN
  * Number in text: 11

### Comparison results (NLTK entity classification, NLTK entity classification + Wikipedia or own patterns + Wikipedia)

In comparison, I would say that it is certainly not possible to compare NLTK entities classification and classification by using the word into Wikipedia. Searching for a pattern definition in Wikipedia and then using it for classification was a great surprise to me. This method seems very successful.

NLTK entity classification works very well, but it can do only a few entities (PERSON, ORGANIZATION, etc.) and not every time it is accurate, but I found errors just in the least cases (Orkney as the person). Compared to Wikipedia, it has a massive advantage in speed.

Wikipedia worked very well, the problem may arise when a given entity has more meanings, where I only take the first one, but this would certainly be a treat and form a dictionary and better indexes. But in such a difficult task of text processing, it seems very successful and could also be used as a basis for further machine learning, for example.

And to use the NLTK entities and my patterns, it is very subjective, because I have focused on all nouns and that is accompanied by an adjective. NLTK selects only some entities as I mentioned above.

I would use the pattern on all the nouns and search results on Wikipedia.

### Implementation

As I mentioned in the repository is attached to a jupyter notebook with implementation. The implementation is structured and described in the notebook itself.
