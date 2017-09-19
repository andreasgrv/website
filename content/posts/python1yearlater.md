title: Python, a year along the way
date: Sunday, 27 September 2015 at 13:14

Recently I've been refactoring some of my code I wrote while learning python
about a year ago.
Needless to say, it is a very painful procedure, grv-pycoder v0.0.1 had some
annoying flaws which are hopefully fixed in the latest version. At this point
I would like to gravely apologize to readers of code of the earlier version,
for grv-pycoder v0.0.2 has also read the code and eeked, leaking 
brain fluid which ran from the ears all the way down to the chin,
dripping repeatedly on the tiled floor, moistening it before congregating
into a small, painstakingly chosen but randomly spatially distributed set of puddles,
that mirrored its confusion and desire for self harm.

So here are the improvements of the latest release of grv-pycoder v0.0.2
including examples.

1.	Does not use indices to access members of a list of tuples that have a
certain meaning encoded into their position.

		:::python
		entities = [('Andreas', (11, 17)), ('Athens', (33, 38))]
		for ent in entities:
			print ent[0]
			print ent[1][0]
			print ent[1][1] 

    Instead it codes (yay!):

		:::python
		entities = [('Andreas', (11, 17)), ('Athens', (33, 38))]
		for entity, (start_offset, end_offset) in entities:
			print(entity)
			print(start_offset)
			print(end_offset)

	> ####Message to v0.0.1
	> Give a name to your variables when you can, people are not machines - when it
	> comes to reading code, they prefer to construe meaning from names,
	> not from arbitrary chosen encodings in sequences - indices.
	> (The irony here that I cannot help but point out, is that language is exactly that,
	>  an encoding of meaning in sequences of tokens. Maybe the word arbitrary is
	>  somewhat more important than it seems)

2.	Does not use what I call java style string concatenation (the + operator) to concatenate 
	strings. Prefers % style string formatting for messages and str.join in most
	other cases.

		:::python
		print name + ' ' + surname + ' is ' + str(age) + ' years old!'
	
	Not as readable as below when you get used to it + you get nice formatting options for numbers.

		:::python
		print('%s %s is %s years old' % (name, surname, age))

	If you have a standard token joiner - then:

		:::python
		print(' '.join((name, surname, str(age))))

	works like a charm - not the case in the above example.

	> ####Message to v0.0.1
	> Choose a string formatting style you like and use it consistently.
	> Avoid java style concatenations, especially when lots of strings are at stake.
	> Use str.join when joining a list or tuple of strings with a common delimiter

3.	Tries to be consistent with python 3 if there is no reason not to.
	There is probably no reason to code:

		:::python
		print 'Hello world'

	instead of

		:::python
		print('Hello world')

	apart from matters of aesthetics and taste. Second version is compatible with python 3 as well as python 2.

	> ####Message to v0.0.1 :
	> Get into habits that you won't need to change later on

4.	Tries to respect 80 character lines. Therefore also handles distributing a single line
	over many lines in a better way.

		:::python
		tagged = dict([(word.upper(), tag) for text, text_tags in zip(texts, tags) for word, tag in zip(text.strip().split(), text_tags)])

	Versus:

		:::python
		tagged = dict([(word.upper(), tag)
					   for text, text_tags in zip(texts, tags)
					   for word, tag in zip(text.strip().split(), text_tags)
					  ])

	> ####Message to v0.0.1
	> Once you understand that splitting lines is inevitable at some point, you will give up
	> on the idea that it is ugly to split lines. Just try to find the cleanest way to do it

5.	Is not as reluctant to using classes, will use them when the code he is writing needs to keep track
	of a state - need to encapsulate data. However, will not go crazy and use classes everywhere.
	grv-pycoder v0.0.1 hated classes so much, because it was a branch of grv-javacoder
	v0.0.2 that used classes even when it only needed a main function. Therefore, the
	class creating module decided to take a year off.


		:::python
		class WikipediaCorpus(object):

			""" Wikipedia corpus representation"""

			def __init__(self, file_stream):
				from os.path import getsize
				# fix wikipedia header - it was incompatible with tree parse xml
				tools.fixformat(file_stream)
				self.file_stream = file_stream
				self.filesize = getsize(file_stream)
				self.bytes_read = 0

			def __iter__(self):
				""" Iterate through wikipedia corpus """
				for event, elem in et.iterparse(self.file_stream):
					# keep track of how much we have read
					if elem.text:
						self.bytes_read += len(elem.text)
					# if we have a text block
					if (event, elem.tag) == ('end', 'text') and elem.text:
						yield elem.text
					elem.clear()

			def __repr__(self):
				""" ipython friendly string representation """
				return ('Wikipedia corpus size (bytes): %s\n'
						'bytes read: %s' % (self.filesize, self.bytes_read))

		with open('en-wikipedia.xml', 'r') as wikifile:
			for text in WikipediaCorpus(wikifile):
				print(text)

	> ####Message to v0.0.1 :
	> Use classes when you need to preserve a state along with your data. 
	> Use python magic functions to make your class api programmer friendly

6.	Creates a setup.py and actually installs the module with **pip install --user -e**.
	Code is no longer scripts in the wild, it dreams to be pushed to some larger
	repository where it can cause more pain.

7.	Still loves list comprehensions and compact code, but tries to explain it along the
	way. Writes more comments. Has however discovered metaprogramming, list and 
	dictionary unpacking and comprehension intermediate variable naming, so may god
	have mercy on our soul xor make his code readable. We don't need gods mercy if he 
	manages to make his code readable.

		:::python
		import json
		import sys
		sys.path.append('mitielib')
		import mitie

		class NamedEntity(object):

			""" Generic Named entity representation """

			def __init__(self, **kwargs):
				for key, val in kwargs.items():
					setattr(self, key, val)

			def __repr__(self):
				return '\n'.join('%s: %s' % (key, val)
								 for (key, val) in self.__dict__.items())

		print('Loading model..')
		ner = mitie.named_entity_extractor('ner_model.dat')
		with open('texts.json', 'r') as json_in:
			# constuct a list of NamedEntity instances from the named entity
			# libraries findings on the json containing the texts
			entities = [NamedEntity(**{'ent': ' '.join([tokens[i] for i in span]),
									   'confidence': confidence,
									   'type': type
									   })
						# get each json
						for line in json_in
						# split text entry of json to tokens
						for tokens in
						# capture tokens in a list, this allows me to 
						# refer to variable tokens succinctly further down
						[json.loads(line)['text'].encode('utf-8').split()]
						# parse it using mitie ner library to get attributes
						for span, type, confidence in
						# capture results in a tuple - this allows me to name them above
						(ner.extract_entities(tokens))
						]
		print(entities)

Amen. 
> #### Message from future self: Eugh.. What was I thinking???
