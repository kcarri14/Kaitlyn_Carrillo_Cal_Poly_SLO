# CSC_482_Project

Description: Given free form text descriptions of some family relations, extract a family tree. The text may be a paragraph or the length of a book.

Deliverables: A command line tool with a text file command line option that can produce the family tree. You should generate both a text format tree, and a graphic tree (to be included in your report), and also output to GED COM format.

Resources: 
Find genealogical records
And/or use wikipedia articles about famous people like Barack Obama
Wikipedia also has some structured facts you might be able to exploit.

Notes: 
GED COM is industry standard format, even though it’s really old and difficult to work with.
Just as important is combining new trees with old trees, if you can make sure the people in them are the same. 
Involves name recognition

- keep track of pronouns too 

- most times wikipedia will mention “obama” -> will usually refer to the person
- only relation for family: brother, mother, sibling, child (no cousins etc.)
    - how many different ways can you say someone is someones mother
- can use ml by getting existing relationship and seeing what words correspond to mother, father, etc. (naive bayes)


# Set Up

1. pip install -r requirements
2. python3 get_wikipedia.py (this will get the wikipedia.json page for your bert classifier)
3. python3 bert_classifier.py
4. `python3 chatBot_bert.py [input_file]` or `python3 chatBot_bert.py` to use command line input.
