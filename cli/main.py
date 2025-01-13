import importlib
import json
import logging
import re
import sys
import tempfile
import time
import warnings
from enum import Enum
from pathlib import Path
from typing import Type

from charset_normalizer import detect
from PIL import Image
from pytesseract import image_to_string
from parsers.text_parser import TextParser
from parsers.docx_parser import DocxParser
from parsers.pdf_parser import PdfParser
from parsers.csv_parser import CSVParser
from converters.markdown_converter import MarkdownConverter
from converters.json_converter import JSONConverter

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class FileType(Enum):
    """Tipos de arquivo suportados."""
    TEXT = "txt"
    DOCX = "docx"
    PDF = "pdf"
    CSV = "csv"
    IMAGE = "image"

class ImageParser:
    """Parser para arquivos de imagem."""
    @staticmethod
    def parse(file_path: Path) -> str:
        try:
            with Image.open(file_path) as img:
                text = image_to_string(img)
            return text
        except Exception as e:
            logging.error(f"Erro ao processar imagem: {e}")
            raise

class FileConverter:
    """Classe principal para gerenciar a conversão de arquivos."""
    PARSERS = {
        FileType.TEXT: TextParser,
        FileType.DOCX: DocxParser,
        FileType.PDF: PdfParser,
        FileType.CSV: CSVParser,
        FileType.IMAGE: ImageParser,
    }

    def __init__(self, input_file: Path, output_dir: Path, output_format: str):
        self.input_file = input_file
        self.output_dir = output_dir
        self.output_format = output_format
        self.file_type = self._detect_file_type()
        self.base_name = self.input_file.stem

    def _detect_file_type(self) -> FileType:
        """
        Detecta o tipo de arquivo com base na extensão.
        """
        ext = self.input_file.suffix.lstrip(".").lower()
        if ext in ["jpg", "jpeg", "png", "bmp", "tiff"]:
            return FileType.IMAGE
        for file_type in FileType:
            if ext == file_type.value:
                return file_type
        raise ValueError(f"Tipo de arquivo não suportado: {ext}")

    def _load_parser(self) -> Type:
        """
        Carrega dinamicamente o parser correspondente ao tipo de arquivo.
        """
        parser_class = self.PARSERS.get(self.file_type)
        if not parser_class:
            raise NotImplementedError(f"Parser para {self.file_type} não implementado.")
        return parser_class()

    def convert(self):
        """
        Realiza a conversão do arquivo de entrada para o formato especificado.
        """
        start_time = time.time()
        logging.info(f"Processando arquivo: {self.input_file}")

        try:
            parser = self._load_parser()
            
            if self.file_type == FileType.TEXT:
                with self.input_file.open("rb") as file:
                    raw_data = file.read()
                    encoding = detect(raw_data)["encoding"]
                with self.input_file.open("r", encoding=encoding) as file:
                    file_stream = file.read()
            elif self.file_type == FileType.IMAGE:
                file_stream = parser.parse(self.input_file)
            else:
                file_stream = self.input_file

            structure = parser.parse(file_stream)

            if self.output_format == "1":
                markdown_converter = MarkdownConverter()
                markdown_content = markdown_converter.convert(structure)
                self._save_file(self.output_dir / f"{self.base_name}.md", markdown_content)
            elif self.output_format == "2":
                json_converter = JSONConverter()
                json_content = json_converter.convert(structure)
                self._save_file(self.output_dir / f"{self.base_name}.json", json_content)

            logging.info(f"Arquivos salvos em: {self.output_dir}")
            logging.info(f"Tempo total de execução: {time.time() - start_time:.2f}s")
        except Exception as e:
            logging.error(f"Erro durante a conversão: {e}")
            raise

    @staticmethod
    def _save_file(file_path: Path, content: str):
        """
        Salva conteúdo em um arquivo.
        """
        try:
            with file_path.open("w", encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo {file_path}: {e}")

def main():
    """
    Função principal do programa de terminal.
    """
    print("=== Conversor de Arquivos ===")
    print("Este programa converte arquivos para os formatos Markdown e JSON.")
    print("Formatos suportados: TXT, DOCX, PDF, CSV, JPG, PNG.")
    print()

    input_file_path = input("Digite o caminho completo do arquivo de entrada: ").strip()
    output_dir_path = input("Digite o caminho completo do diretório de saída: ").strip()
    print("Escolha o formato de saída:")
    print("1 - Markdown")
    print("2 - JSON")
    output_format = input("Digite o número correspondente ao formato desejado: ").strip()

    if output_format not in ["1", "2"]:
        print("Erro: Escolha inválida. Use 1 para Markdown ou 2 para JSON.")
        sys.exit(1)

    input_file = Path(input_file_path)
    output_dir = Path(output_dir_path)

    # Validação de caminhos
    if not input_file.exists() or not input_file.is_file():
        print("Erro: O arquivo de entrada especificado não existe ou é inválido.")
        sys.exit(1)

    if not output_dir.exists() or not output_dir.is_dir():
        warnings.warn(
            "Diretório de saída inválido ou inexistente. Será usado o diretório atual."
        )
        output_dir = Path.cwd()

    # Inicializa e executa o conversor
    try:
        converter = FileConverter(input_file, output_dir, output_format)
        converter.convert()
    except ValueError as ve:
        print(f"Erro: {ve}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
    