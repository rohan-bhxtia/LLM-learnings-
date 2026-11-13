
def chunk_text(full_text):
    chunk_size = 500
    overlap = 50

    chunks = []

    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks
