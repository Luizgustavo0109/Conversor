import io 

class TextParser:
    def parse(self, file_stream):
        if not isinstance(file_stream, io.StringIO):
            raise ValueError("O arquivo deve ser um objeto StringIO.")
        file_stream.seek(0)
        lines = file_stream.getvalue().splitlines()
        return {"type": "text", "content": lines}