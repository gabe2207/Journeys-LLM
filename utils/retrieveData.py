def retrieve_top_matches(query, sections, embeddings, top_n=2):
    # Simula uma correspondência baseada no comprimento da string
    results = []
    for section in sections:
        similarity = len(set(query).intersection(set(section))) / len(set(section))
        results.append((section, similarity))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results[:top_n]
