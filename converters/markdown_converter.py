class MarkdownConverter:
    def convert(self, structure):
        if structure["type"] == "text":
            return "\n".join(structure["content"])
        return f"{structure['type']}\n{''.join(structure['content'])}"