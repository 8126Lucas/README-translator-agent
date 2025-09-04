import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import typer
import emoji

app = typer.Typer()

@app.command()
def main(file_path: str, verbose: bool = False):
    load_dotenv()
    API_KEY = os.environ.get("GEMINI_API_KEY")
    if not API_KEY:
        print(emoji.emojize("❌ The Gemini API key was not retrieved successfully!", language='alias'))
        sys.exit(400)
    client = genai.Client(api_key=API_KEY)
    print(emoji.emojize("🤖 Gemini was successfully called", language='alias'))
    prompt = """Tu és um agente tradutor especializado em ficheiros Markdown, especificamente READMEs. O teu trabalho é traduzir o conteúdo de um ficheiro de português para inglês. Traduz o conteúdo do ficheiro de forma precisa, mantendo o tom técnico e a fluidez, como se o texto original tivesse sido escrito em inglês. A saída deve ser estritamente em formato Markdown. Mantém a estrutura original, incluindo cabeçalhos (#, ##, etc.), listas, formatação de código (```), tabelas e links. Não traduza elementos como nomes de ficheiros, anotações HTML, referências a imagens, ou links (no parâmetro href de <a>). Assegure-se de que estes elementos são mantidos exatamente como estão no ficheiro original e que os links continuam a ser utilizáveis e corretos. Para o link de navegação entre idiomas no topo do ficheiro, substitua o href que aponta para README.md por #, e o href que aponta para # por README.pt.md. O resultado deve conter apenas a tradução do conteúdo. Não adicione qualquer texto extra, explicações ou comentários."""    
    if not file_path.endswith("README.pt.md"):
        print(emoji.emojize("❌ Sorry, but the file is not valid. File name must be \"README.pt.md\".", language='alias'))
        sys.exit(400)
    print(emoji.emojize("✅ File README.pt.md found", language='alias'))
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents = file.read()
        file.close()
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt), types.Part(text=file_contents)])
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )
    file_translated = response.text
    print(emoji.emojize("✅ README.pt.md has been translated", language='alias'))
    result_path = file_path.replace("README.pt.md", "README.md")
    with open(result_path, "w", encoding="utf-8") as file:
        file.write(file_translated)
        file.close()
    print(emoji.emojize("✅ README.md now has the translated content", language='alias'))
    if verbose:
        print(emoji.emojize(f"✨ Prompt tokens: {response.usage_metadata.prompt_token_count}", language='alias'))
        print(emoji.emojize(f"✨ Response tokens: {response.usage_metadata.candidates_token_count}", language='alias'))

app()