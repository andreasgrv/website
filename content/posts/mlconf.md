title: mlconf, a python configuration module with machine learning in mind
date: Monday, 18 September 2017 at 12:58

### Machine Learning configuration - the ugly bits

For my Masters dissertation I compared neural network models for dependency parsing
that used input on the word level to others that constructed the input representation
from characters. Similar to some of my previous machine learning projects,
I soon found the number of settings and hyperparameters I needed to choose and tweak became
larger and larger as the project advanced.
Even after reading about other approaches and how others chose their hyperparameters,
I still felt that most choices can only be reasoned about using trial and error.

<a href="https://github.com/andreasgrv/mlconf" target="_blank">
  <img class="img-responsive"
    src="http://johnny.overfit.xyz/scrat-air.jpg" 
    alt="scrat feeling the direction of the air with his finger"/>
</a>

Given that I could not get away from searching for good hyperparameters --- if the conclusions
from my comparisons of the models were to have any credibility --- it was clear that I was going
to have to spend a large amount of time worrying about these settings.
What bugged me most was that once I had set some reasonable default values for them,
I had no easy way of easily changing them when I wanted to explore variants of my currently favoured approach.

When programming, most of the times you have to make yourself ignore thoughts about suboptimal
features of your code that you cannot fix immediately. At least, this is the case if you want
to stay focussed and get things done. When you stumble upon the same problem a number of times though,
you can no longer overlook it. I feel that many of you may share this feeling.
You can no longer suppress the voice in your head urging you to put an end to this uncomfortable
compromise, this solution you cannot be proud of, this tainted piece of code
that lingers in the background as you unsuccessfully try to move on to something else.
As ardently voiced by Raymond Hettinger:
<a class="brand-symbol" href="https://www.youtube.com/watch?v=wf-BqAjZb8M&feature=youtu.be&t=1401" target="_blank">There must be a better way!!</a>

### So what is a good way ?

One solution would be to use [argparse](https://docs.python.org/3/library/argparse.html) and take advantage
of the [default](https://docs.python.org/3/library/argparse.html#default) setting parameter. I have witnessed this
approach in many projects. However, this only allows you to set a single choice of default settings
for each script. Furthermore, given the fact that the number of options can be greater than 20,
writing the argparse options is tedious and can end up taking up a whole page of code that reads like configuration.
Lastly, I find reading the argparse settings or looking through the output when using --help is much
less clear than reading a configuration file that can contain comments and express structure.

### What is a better way?

I have been a fan of [YAML](http://yaml.org/) for [quite some time now](https://github.com/andreasgrv/tictacs).
I find it is easily readable, it can express structure in a clear way (I might be biased because of python - since it uses indentation)
and it provides a concise snapshot of a machine learning approach. The latter feature is very important if you are into research due to
the importance of reproducibility. By adding all the settings needed into the configuration file, you
can make your results for each experiment easily reproducible. Each configuration file is in a way an experiment.

This is all fine you may say, but how do you easily override the settings you choose in your YAML configuration file?

My approach was to write [mlconf](https://github.com/andreasgrv/mlconf), which dynamically sets argparse entries from a YAML configuration file such
that you can easily override the defaults from the command line. Furthermore, mlconf wraps the returned object into a *Blueprint* object, which
apart from python dictionary semantics also allows getting deep values by chaining the dot operator.

```yaml
# if yaml file contained this
outer:
	inner:
		value: 5


# get the value like this:
bp = Blueprint.from_file(path_to_above)
bp.outer.inner.value # this is 5
```

### Give us an example then..

The following is a toy example of a bag of words model with a SVM classifier.
We will use [scikit-learn](http://scikit-learn.org/stable/) to make this example more realistic.
We therefore need to install mlconf and scikit-learn in order to be able to run it.

#### Installation
```bash
git clone https://github.com/andreasgrv/mlconf
cd mlconf
virtualenv .env && activate .env/bin/activate
pip install .
pip install scikit-learn
```

#### Code

Here are some toy settings that can be found in *tests/data/model.yaml*:
The **vectorizer** entry contains the settings used to create our bag of words,
while the **model** entry specifies the SVM settings. The **$classname** and **$module** entries
are reserved for specifying that this entry can be instantiated using the *build()* method.
As we shall explain soon, the threshold option will be used to determine whether we use a large
or small vocabulary.

```yaml
threshold: 40
vectorizer:
	$classname: CountVectorizer
	$module: sklearn.feature_extraction.text
	lowercase: False
	vocabulary: '?' # we do not know this now (will know after data read)
model:
	$classname: LinearSVC
	$module: sklearn.svm
	loss: 'hinge'
	C: 10
```

The python code we will run can be found in *tests/example.py*. Let's go through it step by step.

We begin by creating an argument parser. We use the mlconf.ArgumentParser class
which extends the original argparse functionality. The mlconf.YAMLLoaderAction action will read
the yaml file we pass to *--load_blueprint* when running the script and allow us to override
all the values of these default attributes by specifying their value after the *--load_blueprint* argument.

```python
import mlconf

parser = mlconf.ArgumentParser(description='A text classifier.')
parser.add_argument('-i', '--input_file', default='README.md')
parser.add_argument('--load_blueprint', action=mlconf.YAMLLoaderAction)

conf = parser.parse_args() # This returns a Blueprint instance with . access
```

We continue by reading our input data (the README.md file) and choose a vocabulary for the bag of words based on the
value of the threshold setting. We normally don't know our vocabulary for the bag of words before reading the data
at runtime. We emulate this effect by choosing which vocabulary to use at runtime.

```python
# set vocab for brevity, normally read from input
sm_vocab = ['acorns', 'tree']
lg_vocab = sm_vocab + ['ice', 'snow']

with open(conf.input_file, 'r') as f:
	lines = f.readlines()

conf.vectorizer.vocabulary = lg_vocab if len(lines) > conf.threshold else sm_vocab
print('Using vocab: %r\n' % conf.vectorizer.vocabulary)
```

We then use the build method to instantiate any class representations we have
in our YAML file. The fact that we only instantiate the CountVectorizer object after we
call the *build* method on the blueprint, means that we can use values for
our classes defined at runtime (such as the vocabulary in our case).

```python
print('%s\n' % conf.vectorizer)       # this is a Blueprint object
built_conf = conf.build()             # instantiate the classes on a copy
print('%s\n' % built_conf.vectorizer) # this is now an instance of CountVectorizer
```

What's next? "Training" of course! We first create our bag of words **X** and then fit
our svm model to predict whether a given line contain the word "scrat".

```python
X = built_conf.vectorizer.fit_transform(lines)

# target is to predict whether scrat is in the line of text
y = ['scrat' in line for line in lines]

built_conf.model.fit(X, y) # fit model
```

Lastly, we use our model to predict whether the samples should contain the word "scrat".

```python
# Predict on other data
samples = ['This is a tree', 'Ice ice baby']
X_test = built_conf.vectorizer.transform(samples)
print('Predicted: %r' % built_conf.model.predict(X_test))
```

In order to run the code we just walked through, you can type:

```bash
python tests/example.py --load_blueprint tests/data/model.yaml
```

On my machine this is what the output looks like:

	:::text
	Using vocab: ['acorns', 'tree', 'ice', 'snow']

	Blueprint:
	  $classname: CountVectorizer
	  $module: sklearn.feature_extraction.text
	  lowercase: false
	  strip_accents: unicode
	  vocabulary:
	  - acorns
	  - tree
	  - ice
	  - snow

	CountVectorizer(analyzer='word', binary=False, decode_error='strict',
			dtype=<class 'numpy.int64'>, encoding='utf-8', input='content',
			lowercase=False, max_df=1.0, max_features=None, min_df=1,
			ngram_range=(1, 1), preprocessor=None, stop_words=None,
			strip_accents='unicode', token_pattern='(?u)\\b\\w\\w+\\b',
			tokenizer=None, vocabulary=['acorns', 'tree', 'ice', 'snow'])

	Predicted: array([False, False], dtype=bool)

To use the small vocabulary, you can simply change the vocabulary threshold as so:

```bash
python tests/example.py --load_blueprint tests/data/model.yaml --threshold 1000
```


Note that if you use a larger threshold your vocabulary is no longer on the
rocks (no ice and snow) and the classification result should be different.

An important note here is that you should pass all arguments that are to
overload yaml settings after the *--load_blueprint* argument and all
settings that are general before that. Eg. *--input_file* should be set
before *--load_blueprint* and *--model.C* after.

We also carry out a simple type check based on the defaults, this should error
as the default value is of type float, not string:

```bash
python tests/example.py --load_blueprint tests/data/model.yaml --model.C scrat
```

While the following will change the svm C to 0.1

```bash
python tests/example.py --load_blueprint tests/data/model.yaml --model.C 0.1
```

Lastly, another handy feature of using mlconf this way is that you can get a list of
the options at the command line using *--help* after the *--load_blueprint* option.

```bash
python tests/example.py --load_blueprint tests/data/model.yaml --help
```

Should output:

```text
usage:  example.py [-h] [-i INPUT_FILE] --load_blueprint BLUEPRINT_FILE
				  [--opt1 val1] [--opt2 val2] ...

YAMLLoader action help: info about arguments you can pass after
--load_blueprint. For more details on global opts use -h or --help before
--load_blueprint.

optional arguments:
  -h, --help            show this help message and exit
  --model.$classname str (default: LinearSVC)
  --model.$module str (default: sklearn.svm)
  --model.C float (default: 10.0)
  --model.loss str (default: hinge)
  --model.penalty str (default: l2)
  --threshold int (default: 40)
  --vectorizer.$classname str (default: CountVectorizer)
  --vectorizer.$module str (default: sklearn.feature_extraction.text)
  --vectorizer.lowercase bool (default: False)
  --vectorizer.strip_accents str (default: unicode)
  --vectorizer.vocabulary str (default: ?)
```

### Drawbacks

On a final note, an important drawback of using mlconf to configure your machine learning approach is that
if you have errors in the configuration they may be harder to debug.
