# pubmed-perplexity
The most surprising results.

# Features
Proof of concept streamlit app.  Uses `biopython` to query pubmed then ranks the results based on title perplexity using GPT2 via the huggingface `evaluate` library.  
The GPT2 based perplexity approach clearly has some quirks and it rates some quite normal looking papers as highly perplexing, but overall I have found this to be an interesting way to discover papers.

# Install in a venv
```
python3 -m venv env
source env/bin/activate
pip install streamlit biopython evaluate torch transformers
```

# Running in the venv
`streamlit run app.py`
On first run it will download the whole of GPT2, which may take a while.

It uses your email to comply with Pubmed's request for this if you make a lot of queries to their server.

# Todo:
- Add direct links to the pubmed article
- Less clunky method of accepting the email
