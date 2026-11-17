import csv
import json
import os
import time
from datetime import datetime
from base_conhecimento import BaseConhecimento


class Assistente:
    def __init__(
        self,
        nome: str,
        base: BaseConhecimento,
        caminho_historico: str = "data/historico.json",
        caminho_csv: str = "data/atendimentos.csv",
    ):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.historico = self._carregar_historico()

    def _carregar_historico(self) -> list:
        if not os.path.exists(self.caminho_historico):
            return []
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return dados if isinstance(dados, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _salvar_historico(self):
        os.makedirs(os.path.dirname(self.caminho_historico), exist_ok=True)
        with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)

    @staticmethod
    def _contem_dado_pessoal(texto: str) -> bool:
        if "@" in texto:
            return True
        qtd_digitos = sum(1 for c in texto if c.isdigit())
        return qtd_digitos >= 8

    @staticmethod
    def _classificar_confianca(pontos: int) -> str:
        if pontos >= 6:
            return "ALTA"
        return "MÉDIA"

    @staticmethod
    def _perguntar_sim_nao(mensagem: str) -> bool:
        while True:
            resp = input(mensagem).strip().lower()
            if resp in ("s", "sim"):
                return True
            if resp in ("n", "nao", "não"):
                return False
            print("Entrada inválida. Digite 's' para sim ou 'n' para não.")

    def registrar(
        self,
        origem: str,
        pergunta: str,
        id_orientacao,
        encontrou: bool,
        ajudou: bool,
        tentativas: int,
        tempo_segundos: float,
    ):
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo_segundos,
        }
        self.historico.append(registro)
        self._salvar_historico()
        self.exportar_csv(silencioso=True)

    def perguntar(self):
        inicio = time.time()
        tentativas = 0

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return

            if not pergunta:
                print("Entrada vazia. Digite sua dúvida ou 0 para voltar.")
                continue

            if self._contem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, RG, placa, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            if not resultados:
                print("\nNão encontrei uma orientação específica para essa dúvida.")
                print("Sugestão: tente palavras como 'cnh', 'licenciamento', 'multa', 'transferir', 'ipva', 'crlv'.")
                print("Categorias disponíveis:", ", ".join(self.base.categorias()))

                tentar_novamente = self._perguntar_sim_nao("Deseja reformular a pergunta? (s/n): ")
                if not tentar_novamente:
                    tempo = round(time.time() - inicio, 1)
                    self.registrar(
                        origem="pergunta",
                        pergunta=pergunta,
                        id_orientacao=None,
                        encontrou=False,
                        ajudou=False,
                        tentativas=tentativas,
                        tempo_segundos=tempo,
                    )
                    return
                continue

            melhor_pontos, melhor_orientacao = resultados[0]
            confianca = self._classificar_confianca(melhor_pontos)
            melhor_orientacao.exibir(pontos=melhor_pontos, nivel_confianca=confianca)

            if len(resultados) > 1:
                print("\nOutras orientações relacionadas:")
                for pts, ori in resultados[1:3]:
                    print(f"  - [{ori.id}] {ori.titulo} ({pts} pontos)")

            ajudou = self._perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar(
                origem="pergunta",
                pergunta=pergunta,
                id_orientacao=melhor_orientacao.id,
                encontrou=True,
                ajudou=ajudou,
                tentativas=tentativas,
                tempo_segundos=tempo,
            )
            return

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Nenhuma categoria disponível.")
            return

        while True:
            print("\n--- Categorias de Trânsito ---")
            for idx, cat in enumerate(categorias, start=1):
                print(f"{idx}. {cat}")
            print("0. Voltar")

            escolha_cat = input("Escolha uma categoria: ").strip()
            if escolha_cat == "0":
                return

            if not escolha_cat.isdigit() or not (1 <= int(escolha_cat) <= len(categorias)):
                print("Opção inválida. Escolha um número da lista.")
                continue

            categoria_selecionada = categorias[int(escolha_cat) - 1]
            itens = self.base.por_categoria(categoria_selecionada)

            while True:
                print(f"\n--- {categoria_selecionada} ---")
                for idx, ori in enumerate(itens, start=1):
                    print(f"{idx}. {ori.titulo}")
                print("0. Voltar")

                inicio = time.time()
                escolha_ori = input("Escolha uma orientação: ").strip()
                if escolha_ori == "0":
                    break

                if not escolha_ori.isdigit() or not (1 <= int(escolha_ori) <= len(itens)):
                    print("Opção inválida. Escolha um número da lista.")
                    continue

                orientacao = itens[int(escolha_ori) - 1]
                orientacao.exibir()
                ajudou = self._perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                tempo = round(time.time() - inicio, 1)

                self.registrar(
                    origem="categoria",
                    pergunta=f"Categoria: {categoria_selecionada}",
                    id_orientacao=orientacao.id,
                    encontrou=True,
                    ajudou=ajudou,
                    tentativas=1,
                    tempo_segundos=tempo,
                )
                return

    def indicadores(self, nota_facilidade: int = None):
        total = len(self.historico)
        print("\n" + "=" * 55)
        print(f"INDICADORES DE ATENDIMENTO - {self.nome}")
        print("=" * 55)

        if total == 0:
            print("Nenhum atendimento registrado até o momento.")
            print("=" * 55)
            return

        encontrados = [r for r in self.historico if r.get("encontrou")]
        ajudaram = [r for r in self.historico if r.get("ajudou")]
        nao_resolvidas = [r["pergunta"] for r in self.historico if not r.get("encontrou")]

        taxa_encontrada = (len(encontrados) / total) * 100
        taxa_acerto = (len(ajudaram) / total) * 100
        tempo_medio = (
            sum(r.get("tempo_segundos", 0) for r in encontrados) / len(encontrados)
            if encontrados
            else 0.0
        )
        media_tentativas = sum(r.get("tentativas", 1) for r in self.historico) / total

        print(f"Total de atendimentos:     {total}")
        print(f"Resposta encontrada (%):   {taxa_encontrada:.1f}%")
        print(f"Taxa de acerto: ajudou (%): {taxa_acerto:.1f}%")
        print(f"Tempo médio para encontrar: {tempo_medio:.1f}s")
        print(f"Tentativas por atendimento: {media_tentativas:.1f}")
        if nota_facilidade is not None:
            print(f"Facilidade de uso (1 a 5):  {nota_facilidade}/5")
        else:
            print("Facilidade de uso (1 a 5):  Avaliada ao encerrar")

        print("\nLista de dúvidas sem solução:")
        if nao_resolvidas:
            for duvida in nao_resolvidas:
                print(f"  - {duvida}")
        else:
            print("  (Nenhuma dúvida sem solução)")
        print("=" * 55)

    def exportar_csv(self, silencioso: bool = False):
        os.makedirs(os.path.dirname(self.caminho_csv), exist_ok=True)
        colunas = [
            "data",
            "origem",
            "pergunta",
            "id_orientacao",
            "encontrou",
            "ajudou",
            "tentativas",
            "tempo_segundos",
        ]
        with open(self.caminho_csv, "w", newline="", encoding="utf-8") as arquivo_csv:
            writer = csv.DictWriter(arquivo_csv, fieldnames=colunas)
            writer.writeheader()
            for item in self.historico:
                writer.writerow({col: item.get(col, "") for col in colunas})

        if not silencioso:
            print(f"Histórico exportado com sucesso para '{self.caminho_csv}'.")
