 # CONVEC - Ferramenta de Conversão de Arquivos  

## Visão Geral

File Converter é uma ferramenta desenvolvida em Python para realizar a conversão de diversos tipos de arquivos em formatos estruturados, como Markdown e JSON. E
la oferece suporte a documentos de texto, planilhas, PDFs, imagens e outros formatos comumente utilizados. O objetivo do projeto é simplificar a extração e transformação 
de dados para processamento ou armazenamento em formatos legíveis e compatíveis com máquinas.

## Funcionalidades

***Suporte a Tipos de Arquivo:***

* Arquivos de texto (.txt)
* Documentos do Microsoft Word (.docx)
* Documentos PDF (.pdf)
* Arquivos CSV (.csv)
* Imagens (.jpg, .jpeg, .png, .bmp, .tiff) com OCR (Reconhecimento Óptico de Caracteres).

## Formatos de Saída:

       Markdown (.md)
       JSON (.json)

* **Análise Dinâmica:** Carrega dinamicamente parsers específicos para cada tipo de arquivo.
* **Tratamento de Erros:** Gerencia exceções de forma robusta, garantindo que arquivos inválidos ou tipos não suportados sejam tratados adequadamente.
* **Registro de Logs:** Logs detalhados para monitorar o processo de conversão.

## Como Funciona

1. **Detecção de Arquivo:** Identifica automaticamente o tipo do arquivo de entrada com base na sua extensão.
2. **Análise:** Utiliza parsers especializados para cada tipo de arquivo para extrair os dados.
3. **Conversão:** Converte os dados extraídos para o formato escolhido (*Markdown* ou *JSON*).
4. **Saída:** Salva os arquivos convertidos no diretório especificado.
