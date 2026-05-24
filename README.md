# Desafio na Cozinha - Pablo e Vinícius

Trabalho de Algoritmos e Estruturas de Dados II focado na organização e integridade de receitas.

## Recuperação de Questão da Prova
**Questão Escolhida:** Questão 5 (Algoritmos Gulosos).

### Motivo e Implementação
Escolhemos recuperar a questão 5 pois a nossa principal dificuldade no momento da prova foi a **falta de tempo** para estruturar a lógica e concluir a questão.

Para resolver esse problema no trabalho, implementamos um algoritmo guloso na função `generateRecipeCombination`. O sistema gera um menu completo com base no objetivo escolhido (ser econômico ou ser rápido). O programa ordena as receitas pelo critério definido e vai adicionando cada uma ao menu enquanto o custo ou o tempo total não ultrapassar o limite que o usuário informou.

### Como Testar
1. Execute o programa: `python3 main.py`
2. No menu principal, escolha a opção **2** (Chef Mode).
3. Em seguida, escolha a opção **2** (Generate Recipe Combination).
4. Selecione o objetivo: **1** (Economic) ou **2** (Fast).
5. Informe os valores máximos de custo (ex: 100) e de tempo (ex: 120).
6. O sistema listará as receitas selecionadas pela estratégia gulosa.

---

## Estruturas de Dados Implementadas
As estruturas principais foram isoladas na pasta `dataStructures` para melhor organização:

* **Tabela Hash (`hashTable.py`):** Utilizada para armazenar as receitas por ID e para buscas rápidas por categoria e ingrediente. Possui redimensionamento dinâmico automático.
* **Árvore Trie (`trie.py`):** Utilizada para a busca por nome. Permite encontrar receitas a partir de um prefixo digitado.
* **Árvore B (`bTree.py`):** Utilizada para organizar as receitas por critérios numéricos como preço, avaliação e tempo, permitindo filtragens eficientes.
* **Algoritmo Guloso:** Conforme detalhado na seção de recuperação acima.

## Segurança (Integridade)
Cada receita possui um hash SHA-256 gerado a partir de suas informações. No "Modo Investigação", o programa verifica se o conteúdo atual condiz com o hash salvo. Qualquer alteração manual nos arquivos `recipes.json` ou `recipes2.json` será detectada pelo sistema.

## Fonte de Dados
O sistema utiliza arquivos JSON estáticos (`recipes.json` e `recipes2.json`) contendo receitas geradas por IA, com todos os dados necessários para os testes de custo, tempo e avaliação.

## Execução
Basta utilizar o comando:
```bash
python3 main.py
```
