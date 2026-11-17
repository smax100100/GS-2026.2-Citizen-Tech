from base_conhecimento import BaseConhecimento
from assistente import Assistente


def solicitar_nota_facilidade() -> int:
    while True:
        nota = input("\nAntes de sair, avalie a facilidade de uso (1 a 5): ").strip()
        if nota.isdigit() and 1 <= int(nota) <= 5:
            return int(nota)
        print("Entrada inválida. Digite um número inteiro de 1 a 5.")


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível iniciar o assistente sem uma base de conhecimento válida.")
        return

    assistente = Assistente("Citizen Assist AI - Despachante de Trânsito", base)

    while True:
        print("\n" + "=" * 55)
        print(f"  {assistente.nome}")
        print("=" * 55)
        print("1. Fazer uma pergunta (busca inteligente)")
        print("2. Navegar por categorias")
        print("3. Ver indicadores de atendimento")
        print("4. Exportar atendimentos para CSV")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            nota = solicitar_nota_facilidade()
            assistente.indicadores(nota_facilidade=nota)
            assistente.exportar_csv()
            print("Encerrando o Citizen Assist AI. Até logo!")
            break
        else:
            print("Opção inválida. Escolha 1, 2, 3, 4 ou 0.")


if __name__ == "__main__":
    main()
