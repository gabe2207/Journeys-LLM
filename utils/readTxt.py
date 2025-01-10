def load_and_split_document(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content.split("\n\n")  # Divide o conteúdo em seções
