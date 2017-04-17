# LSA
Vector based semantic analysis

This technique is a simple implementation of Latent Semantic Indexing to perform search queries.  Given a set of 100+ documents,
the files included will process the documents by stemming and truncating them, transform them into term document vectors, 
and perform a Singular Value Decomposition which removes noisy data and allows for a clearer image of how documents or 
terms are related.  This technique is commonly used in search engines.
