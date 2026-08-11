"""
Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento
--------------------------------------------------------------------------
Sistema em Python que simula a inspeção automática de qualidade de peças
em uma linha de montagem industrial, com armazenamento em caixas de
capacidade limitada e geração de relatórios consolidados.

Autor: Diego Colombari Rapichan
Disciplina: Algoritmos e Lógica de Programação
"""

from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Regras de qualidade (critérios de aprovação)
# ---------------------------------------------------------------------------
PESO_MIN = 95.0
PESO_MAX = 105.0
CORES_ACEITAS = {"azul", "verde"}
COMPRIMENTO_MIN = 10.0
COMPRIMENTO_MAX = 20.0
CAPACIDADE_CAIXA = 10


# ---------------------------------------------------------------------------
# Entidades
# ---------------------------------------------------------------------------
@dataclass
class Peca:
    """Representa uma peça produzida na linha de montagem."""
    id: str
    peso: float
    cor: str
    comprimento: float
    status: str = ""          # "Aprovada" ou "Reprovada"
    motivo: str = ""          # motivo da reprovação (se houver)
    caixa: Optional[int] = None  # número da caixa em que foi armazenada


@dataclass
class Caixa:
    """Representa uma caixa de armazenamento de peças aprovadas."""
    numero: int
    pecas: List[Peca] = field(default_factory=list)
    fechada: bool = False

    def cheia(self) -> bool:
        return len(self.pecas) >= CAPACIDADE_CAIXA


# ---------------------------------------------------------------------------
# Núcleo do sistema
# ---------------------------------------------------------------------------
class SistemaGestao:
    """Controla o cadastro, avaliação, armazenamento e relatórios das peças."""

    def __init__(self):
        self.pecas: List[Peca] = []
        self.caixas: List[Caixa] = [Caixa(numero=1)]

    # -- avaliação de qualidade -------------------------------------------------
    @staticmethod
    def avaliar_peca(peso: float, cor: str, comprimento: float):
        """Aplica as regras de qualidade e retorna (aprovada, motivo)."""
        motivos = []

        if not (PESO_MIN <= peso <= PESO_MAX):
            motivos.append(f"peso fora do intervalo ({PESO_MIN}g-{PESO_MAX}g)")

        if cor.lower() not in CORES_ACEITAS:
            motivos.append("cor não aceita (deve ser azul ou verde)")

        if not (COMPRIMENTO_MIN <= comprimento <= COMPRIMENTO_MAX):
            motivos.append(
                f"comprimento fora do intervalo ({COMPRIMENTO_MIN}cm-{COMPRIMENTO_MAX}cm)"
            )

        if motivos:
            return False, "; ".join(motivos)
        return True, ""

    # -- caixa atual --------------------------------------------------------
    def _caixa_atual(self) -> Caixa:
        return self.caixas[-1]

    def _armazenar(self, peca: Peca):
        """Coloca uma peça aprovada na caixa atual, fechando-a se necessário."""
        caixa = self._caixa_atual()
        caixa.pecas.append(peca)
        peca.caixa = caixa.numero

        if caixa.cheia():
            caixa.fechada = True
            nova_caixa = Caixa(numero=caixa.numero + 1)
            self.caixas.append(nova_caixa)

    # -- 1. cadastrar nova peça ----------------------------------------------
    def cadastrar_peca(self, id_peca: str, peso: float, cor: str, comprimento: float) -> Peca:
        if any(p.id == id_peca for p in self.pecas):
            raise ValueError(f"Já existe uma peça cadastrada com o id '{id_peca}'.")

        aprovada, motivo = self.avaliar_peca(peso, cor, comprimento)
        peca = Peca(
            id=id_peca,
            peso=peso,
            cor=cor,
            comprimento=comprimento,
            status="Aprovada" if aprovada else "Reprovada",
            motivo=motivo,
        )

        if aprovada:
            self._armazenar(peca)

        self.pecas.append(peca)
        return peca

    # -- 2. listar peças aprovadas/reprovadas --------------------------------
    def listar_pecas(self, filtro: Optional[str] = None) -> List[Peca]:
        """filtro pode ser None (todas), 'Aprovada' ou 'Reprovada'."""
        if filtro is None:
            return list(self.pecas)
        return [p for p in self.pecas if p.status == filtro]

    # -- 3. remover peça cadastrada -------------------------------------------
    def remover_peca(self, id_peca: str) -> bool:
        peca = next((p for p in self.pecas if p.id == id_peca), None)
        if peca is None:
            return False

        # Se a peça estava armazenada em uma caixa, remove de lá também.
        if peca.caixa is not None:
            for caixa in self.caixas:
                if caixa.numero == peca.caixa and peca in caixa.pecas:
                    caixa.pecas.remove(peca)
                    # Uma caixa que já foi fechada não é reaberta automaticamente;
                    # isso preserva o histórico de produção já consolidado.
                    break

        self.pecas.remove(peca)
        return True

    # -- 4. listar caixas fechadas -------------------------------------------
    def listar_caixas_fechadas(self) -> List[Caixa]:
        return [c for c in self.caixas if c.fechada]

    # -- 5. gerar relatório final ---------------------------------------------
    def gerar_relatorio(self) -> dict:
        aprovadas = self.listar_pecas("Aprovada")
        reprovadas = self.listar_pecas("Reprovada")
        caixas_fechadas = self.listar_caixas_fechadas()

        motivos_reprovacao = {}
        for p in reprovadas:
            motivos_reprovacao[p.id] = p.motivo

        return {
            "total_aprovadas": len(aprovadas),
            "total_reprovadas": len(reprovadas),
            "motivos_reprovacao": motivos_reprovacao,
            "quantidade_caixas_utilizadas": len(caixas_fechadas) + (
                1 if self._caixa_atual().pecas else 0
            ),
            "caixas_fechadas": len(caixas_fechadas),
        }


# ---------------------------------------------------------------------------
# Interface de linha de comando (menu interativo)
# ---------------------------------------------------------------------------
def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print(">> Valor inválido. Digite um número (ex: 98.5).")


def menu():
    sistema = SistemaGestao()

    opcoes = """
========================================
  SISTEMA DE GESTÃO DE PEÇAS - LINHA DE MONTAGEM
========================================
1. Cadastrar nova peça
2. Listar peças aprovadas/reprovadas
3. Remover peça cadastrada
4. Listar caixas fechadas
5. Gerar relatório final
0. Sair
========================================
"""

    while True:
        print(opcoes)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n-- Cadastro de nova peça --")
            id_peca = input("ID da peça: ").strip()
            if not id_peca:
                print(">> ID não pode ser vazio.")
                continue
            peso = ler_float("Peso (g): ")
            cor = input("Cor: ").strip()
            comprimento = ler_float("Comprimento (cm): ")

            try:
                peca = sistema.cadastrar_peca(id_peca, peso, cor, comprimento)
            except ValueError as e:
                print(f">> Erro: {e}")
                continue

            if peca.status == "Aprovada":
                print(f">> Peça '{peca.id}' APROVADA e armazenada na caixa {peca.caixa}.")
            else:
                print(f">> Peça '{peca.id}' REPROVADA. Motivo: {peca.motivo}")

        elif opcao == "2":
            print("\n-- Listagem de peças --")
            print("1. Todas  2. Apenas aprovadas  3. Apenas reprovadas")
            sub = input("Escolha: ").strip()
            filtro = {"1": None, "2": "Aprovada", "3": "Reprovada"}.get(sub, None)
            pecas = sistema.listar_pecas(filtro)

            if not pecas:
                print(">> Nenhuma peça encontrada.")
            for p in pecas:
                info = f"ID: {p.id} | Peso: {p.peso}g | Cor: {p.cor} | Comp: {p.comprimento}cm | Status: {p.status}"
                if p.status == "Aprovada":
                    info += f" | Caixa: {p.caixa}"
                else:
                    info += f" | Motivo: {p.motivo}"
                print(info)

        elif opcao == "3":
            print("\n-- Remoção de peça --")
            id_peca = input("ID da peça a remover: ").strip()
            if sistema.remover_peca(id_peca):
                print(f">> Peça '{id_peca}' removida com sucesso.")
            else:
                print(f">> Peça '{id_peca}' não encontrada.")

        elif opcao == "4":
            print("\n-- Caixas fechadas --")
            caixas = sistema.listar_caixas_fechadas()
            if not caixas:
                print(">> Nenhuma caixa fechada ainda.")
            for c in caixas:
                ids = ", ".join(p.id for p in c.pecas)
                print(f"Caixa {c.numero} | {len(c.pecas)} peças | IDs: {ids}")

        elif opcao == "5":
            print("\n-- Relatório final --")
            r = sistema.gerar_relatorio()
            print(f"Total de peças aprovadas: {r['total_aprovadas']}")
            print(f"Total de peças reprovadas: {r['total_reprovadas']}")
            if r["motivos_reprovacao"]:
                print("Motivos de reprovação:")
                for id_peca, motivo in r["motivos_reprovacao"].items():
                    print(f"  - {id_peca}: {motivo}")
            print(f"Quantidade de caixas utilizadas: {r['quantidade_caixas_utilizadas']}")
            print(f"  (sendo {r['caixas_fechadas']} já fechadas)")

        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break

        else:
            print(">> Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
