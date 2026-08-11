# Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento

Sistema em Python que simula a inspeção automática de qualidade de peças em uma linha de montagem industrial, substituindo o processo manual por regras lógicas de aprovação, armazenamento em caixas de capacidade limitada e geração de relatórios consolidados.

## Funcionamento

O sistema recebe os dados de cada peça (**id**, **peso**, **cor** e **comprimento**) e avalia automaticamente se ela está **aprovada** ou **reprovada**, segundo os critérios de qualidade:

| Critério     | Faixa aceita        |
|--------------|----------------------|
| Peso         | entre 95g e 105g     |
| Cor          | azul ou verde        |
| Comprimento  | entre 10cm e 20cm    |

- Peças **aprovadas** são armazenadas em **caixas de 10 peças**. Ao atingir a capacidade máxima, a caixa é **fechada** automaticamente e uma nova caixa é iniciada.
- Peças **reprovadas** não são armazenadas, mas o motivo da reprovação é registrado.
- O sistema gera um **relatório final** com total de aprovadas, total de reprovadas (com motivo), e quantidade de caixas utilizadas.

## Estrutura do código

- `Peca`: representa cada peça produzida (dataclass).
- `Caixa`: representa uma caixa de armazenamento, com capacidade limitada.
- `SistemaGestao`: classe central com toda a lógica de cadastro, avaliação, armazenamento, remoção e geração de relatórios.
- `menu()`: interface de linha de comando (CLI) interativa.

## Como rodar o programa

Pré-requisito: Python 3.8 ou superior (não usa bibliotecas externas).

```bash
python3 sistema.py
```

O menu interativo será exibido no terminal:

```
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
```

## Exemplos de entrada e saída

### Cadastro de peça aprovada

```
Escolha uma opção: 1

-- Cadastro de nova peça --
ID da peça: P001
Peso (g): 100
Cor: azul
Comprimento (cm): 15
>> Peça 'P001' APROVADA e armazenada na caixa 1.
```

### Cadastro de peça reprovada

```
Escolha uma opção: 1

-- Cadastro de nova peça --
ID da peça: P002
Peso (g): 90
Cor: vermelho
Comprimento (cm): 25
>> Peça 'P002' REPROVADA. Motivo: peso fora do intervalo (95.0g-105.0g); cor não aceita (deve ser azul ou verde); comprimento fora do intervalo (10.0cm-20.0cm)
```

### Relatório final

```
Escolha uma opção: 5

-- Relatório final --
Total de peças aprovadas: 11
Total de peças reprovadas: 1
Motivos de reprovação:
  - P002: peso fora do intervalo (95.0g-105.0g); cor não aceita (deve ser azul ou verde); comprimento fora do intervalo (10.0cm-20.0cm)
Quantidade de caixas utilizadas: 2
  (sendo 1 já fechadas)
```

## Autor

Diego Colombari Rapichan — Pós-graduação em IA & Automação Digital (UniFECAF)
