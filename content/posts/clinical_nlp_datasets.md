title: Clinical NLP datasets
date: Sunday, 8 March 2020 at 22:58

### Datasets useful for clinical Natural Language Processing (NLP)

For the past year I have been working on NLP models for information extraction from clinical texts.
It has been challenging to find relevant/in-domain available annotated datasets, so below I'm tabulating some resources I have found useful, annotated by NLP task, in the hope that these may be useful to other lonely souls navigating the desolate oceans of <q>big data</q>.

### Data source: Biomedical articles/papers

These datasets contain text that is quite different from clinical text, however the datasets are publically available and in my experience contain vocabulary overlap with a clinical vocabulary of interest.

* [Genia](https://github.com/allenai/genia-dependency-trees/tree/master/stanford)
<span class="badge blue">Part of Speech</span>
<span class="badge cyan">Parsing</span>

* [CRAFT](https://github.com/UCDenver-ccp/CRAFT/tree/master/structural-annotation/dependency/conllu)
<span class="badge blue">Part of Speech</span>
<span class="badge cyan">Parsing</span>

* [Elsevier](https://github.com/elsevierlabs/OA-STM-Corpus/blob/master/Treebank/Merged/S2213158213001253-Medicine-merged.pretty)
<span class="badge blue">Part of Speech</span>
<span class="badge cyan">Parsing</span>
Medicine publications (421 sentences). The tags used may be non-standard.

* [MedMentions](https://github.com/chanzuckerberg/MedMentions)
<span class="badge" style="background-color: #b2df8a">Named Entities</span>

### Data source: Clinical data

All clinical datasets below are not publically available. Most can be requested / made available to researchers by following instructions on the corresponding dataset webpage.
<!-- # Thyme Corpus aka MiPACQ Treebank (needs sign DUA and request access) -->

* [Thyme/MiPACQ Treebank](https://clear.colorado.edu/TemporalWiki/index.php/Main_Page)
<span class="badge cyan">Parsing</span>
<span class="badge olive">Named Entities</span>

* [i2b2](https://www.i2b2.org/NLP/DataSets/Main.php)
<span class="badge olive">Named Entities</span>
<span class="badge green">Relations</span>
<span class="badge red">Negation + Uncertainty</span>

* [Fan et al](https://sourceforge.net/projects/medicaltreebank)
<span class="badge cyan">Parsing</span>
This is a subpart of the i2b2 data annotated for constituency parsing, as described in the following [paper](https://academic.oup.com/jamia/article/20/6/1168/704361).
**NOTE**: Click on files and download **wordfreak_annotation_files.zip** - the default download is a single file. The downloaded files include annotations with text offsets that need to be linked with corresponding files in the [i2b2](https://www.i2b2.org/NLP/DataSets/Main.php) dataset.

* [n2c2](https://n2c2.dbmi.hms.harvard.edu/track3)
<span class="badge olive">Named Entities</span>
An extension to the i2b2 dataset that links entity spans to UMLS concepts
released as part of the 2019 n2c2 challenge on clinical concept normalisation. The data should be available on request (at some point in 2020).

* [Bioscope](https://rgai.inf.u-szeged.hu/node/105)
<span class="badge red">Negation + Uncertainty</span>
The [paper](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-S11-S9) introducing the dataset.
The dataset is constructed from 3 different sources: Abstracts of the Genia corpus, Full scientific articles, and
Clinical free-texts. The radiology report corpus used was from the [CMC clinical coding challenge](https://ncc.cchmc.org/prod/pestianlabdata/request.do).

* [MIMIC-III](https://mimic.physionet.org/)
<span class="badge orange">Raw text</span>
<span class="badge purple">Document labels</span>
MIMIC, in addition to a lot of clinical raw text contains documents annotated with ICD-9 codes.

* [MIMIC-CXR](https://physionet.org/content/mimic-cxr/2.0.0/)
<span class="badge orange">Raw text</span>
This release contains radiology reports with their corresponding images.
Some relevant code resources are available on [github](https://github.com/MIT-LCP/mimic-cxr).

* [IU radiology report dataset](https://openi.nlm.nih.gov/imgs/collections/NLMCXR_reports.tgz)
<span class="badge orange">Raw text</span>
This is a dataset of chest radiology reports from the Indiana University hospital network. There is also a dataset of images [available](https://openi.nlm.nih.gov/faq#collection).

* [Kim et al.](https://doi.org/10.1371/journal.pone.0212778.s002)
<span class="badge orange">Raw text</span>
<span class="badge purple">Document labels</span>
A dataset of brain radiology reports labelled for acute ischemic stroke. The dataset was published along with their paper: [Natural language processing and machine learning algorithm to identify brain MRI reports with acute ischemic stroke](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0212778).

Additional resources can be found on the [Clinical NLP Workshop page](https://clinical-nlp.github.io/2019/resources.html).

Thanks to [Hang Dong](https://cgi.csc.liv.ac.uk/~hang/) for his feedback and for pointing out additional resources.
