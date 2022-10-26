# NLI Abstract Dataset

This dataset is composed of a selection of abstracts of scientific papers from the [OpenAIRE Research Graph Dumps](https://graph.openaire.eu/develop/graph-dumps.html).

The selection is made to build a dataset to test Native Language Identification (NLI) methods. This dataset can be given in input to the code of the [NLI explain](https://github.com/aesuli/nli_explain) repo.

A NLI problem requires to identify the native language of the writer of a piece of text written in a second language.

The second language of this dataset is English.
The native languages of the writers are:
Turkish, German, Spanish, Latvian, Italian, French, Portuguese, Russian, Dutch, Japanese, Polish, Finnish, and Danish.

The selection of abstracts and their association to a native language is made heuristically, using the following set of rules:

- the entry in the OpenAIRE catalog must have a single author.
- the type of entry must one in: Article, Conference object, Preprint, Doctoral thesis, Master thesis, Thesis, Bachelor thesis.
- the description field must have exactly two fields.
- the length of text in the fields must be between 300 and 3000 characters.
- one of the fields must be identified as English by langId.
- the language identified by landId for the other field determines the native language.

These selection rules select 263206 entries out of the 160M in the OpenAIRE dump.

A second script selects native English abstracts, which appears to be a harder task. The constraints in this selection are:
- the entry in the OpenAIRE catalog must have a single author.
- the type of entry must one in: Article, Conference object, Preprint, Doctoral thesis, Master thesis, Thesis, Bachelor thesis.
- the description field must have exactly one fields.
- the length of text in the fields must be between 300 and 3000 characters.
- the field must be identified as English by langId.
- the field 'country' in the entry must be 'en'.

These selection rules select 136428 entries.

Specially these second set of constraints do not guarantee a strict selection of native writers, yet the selection of abstracts seems good in general.
Comments are very welcome on how to improve the quality of selection.
