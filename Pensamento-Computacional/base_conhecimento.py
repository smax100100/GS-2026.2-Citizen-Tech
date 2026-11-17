import json
import os
from orientacao import Orientacao

ACENTOS = {
    "á": "a", "à": "a", "ã": "a", "â": "a",
    "é": "e", "ê": "e",
    "í": "i",
    "ó": "o", "õ": "o", "ô": "o",
    "ú": "u",
    "ç": "c",
}


def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()[]{}-_/\\\"'":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho: str):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self) -> bool:
        self.orientacoes = []
        if not os.path.exists(self.caminho):
            print(f"[Erro] Arquivo não encontrado: {self.caminho}")
            return False

        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if not isinstance(dados, list):
                print("[Erro] Estrutura inválida no JSON: esperada uma lista.")
                return False

            campos_obrigatorios = {
                "id", "categoria", "titulo", "palavras_chave",
                "resposta", "documentos", "onde", "fonte", "verificado_em"
            }

            for item in dados:
                if not isinstance(item, dict) or not campos_obrigatorios.issubset(item.keys()):
                    continue
                orientacao = Orientacao(
                    id=item["id"],
                    categoria=item["categoria"],
                    titulo=item["titulo"],
                    palavras_chave=item["palavras_chave"],
                    resposta=item["resposta"],
                    documentos=item["documentos"],
                    onde=item["onde"],
                    fonte=item["fonte"],
                    verificado_em=item["verificado_em"],
                )
                self.orientacoes.append(orientacao)

            return len(self.orientacoes) > 0

        except (json.JSONDecodeError, OSError) as erro:
            print(f"[Erro] Falha ao ler a base de conhecimento: {erro}")
            return False

    def categorias(self) -> list:
        lista_categorias = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista_categorias:
                lista_categorias.append(orientacao.categoria)
        return lista_categorias

    def por_categoria(self, categoria: str) -> list:
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta_norm: str, orientacao: Orientacao) -> int:
        pontos = 0
        palavras_pergunta = set(pergunta_norm.strip().split())

        for kw in orientacao.palavras_chave:
            kw_norm = normalizar(kw)
            termos_kw = set(kw_norm.strip().split())
            if kw_norm.strip() and (kw_norm in pergunta_norm or termos_kw.issubset(palavras_pergunta)):
                pontos += 3

        titulo_norm = normalizar(orientacao.titulo)
        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and f" {palavra} " in titulo_norm:
                pontos += 1

        return pontos

    def buscar(self, pergunta: str) -> list:
        pergunta_norm = normalizar(pergunta)
        resultados = []

        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta_norm, orientacao)
            if pontos >= 3:
                resultados.append((pontos, orientacao))

        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados
