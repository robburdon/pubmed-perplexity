import os
import streamlit as st
from Bio import Entrez
from evaluate import load

class PubMedFetcher:
    def __init__(self, email):
        self.email = email
        Entrez.email = email

    def search_pubmed(self, query, max_results, db="pubmed"):
        """Search PubMed and return a list of IDs for the matching papers."""
        try:
            handle = Entrez.esearch(db=db, term=query, retmax=max_results)
            record = Entrez.read(handle)
        except Exception as e:
            st.error(f"Failed to search PubMed: {e}")
            return []
        finally:
            handle.close()
        return record["IdList"]

    def fetch_titles_and_PMIDs(self, pubmed_ids, db="pubmed"):
        """Fetch the titles and PMIDs for a list of PubMed IDs."""
        id_list = ",".join(pubmed_ids)
        try:
            handle = Entrez.efetch(db=db, id=id_list, rettype="xml")
            records = Entrez.read(handle)
        except Exception as e:
            st.error(f"Failed to fetch PubMed data: {e}")
            return []
        finally:
            handle.close()
        return [(r["MedlineCitation"]["Article"]["ArticleTitle"], r["MedlineCitation"]["PMID"]) for r in records["PubmedArticle"]]

def calculate_perplexity(titles, model_id='gpt2'):
    """Calculate the perplexity for a list of titles."""
    try:
        perplexity = load("perplexity", module_type="metric")
        results = perplexity.compute(model_id=model_id, add_start_token=True, predictions=titles)
    except Exception as e:
        st.error(f"Failed to calculate perplexity: {e}")
        return []
    return results["perplexities"]

st.title("PubMed search by Maximum Perplexity")
st.subheader("The most surprising titles for your query")

query = st.text_input("Enter your search query:")
max_results = st.slider("Maximum number of results:", 1, 100, 10)
pubmed_email = st.text_input("Enter your email address (for Pubmed access):")

pubmed_fetcher = PubMedFetcher(pubmed_email)

if st.button("Fetch and rank papers"):
    with st.spinner('Searching papers...'):
        pubmed_ids = pubmed_fetcher.search_pubmed(query, max_results)
    with st.spinner('Fetching paper titles...'):
        paper_titles = pubmed_fetcher.fetch_titles_and_PMIDs(pubmed_ids)
    with st.spinner('Calculating perplexities...'):
        title_texts = [title for title, _ in paper_titles]
        perplexities = calculate_perplexity(title_texts)
    with st.spinner('Ranking papers...'):
        sorted_titles_perplexity = sorted(zip(paper_titles, perplexities), key=lambda x: x[1], reverse=True)

    st.subheader("Ranked Papers:")
    for (title, pmid), perplexity in sorted_titles_perplexity:
        st.write(f"{title} (PMID: {pmid})")
        st.write(f"Perplexity: {perplexity:.2f}")
        st.write("---")
