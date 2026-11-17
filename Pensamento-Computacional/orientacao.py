class Orientacao:
    def __init__(
        self,
        id: int,
        categoria: str,
        titulo: str,
        palavras_chave: list,
        resposta: str,
        documentos: list,
        onde: str,
        fonte: str,
        verificado_em: str,
    ):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self, pontos: int = None, nivel_confianca: str = None):
        print("\n" + "=" * 65)
        if nivel_confianca is not None and pontos is not None:
            print(f"Confiança da resposta: {nivel_confianca} ({pontos} pontos)")
        print(f">> {self.titulo}  [{self.categoria}]")
        print(f"{self.resposta}")
        print("\nDocumentos necessários:")
        for doc in self.documentos:
            print(f"  - {doc}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print("Aviso: este assistente NÃO é um canal oficial.")
        print("=" * 65)
