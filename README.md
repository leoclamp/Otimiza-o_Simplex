# Otimização utilizando o Método Simplex com Interface Gráfica

Este projeto implementa uma aplicação gráfica para resolver problemas de Programação Linear utilizando o Método Simplex. Desenvolvido em Python com as bibliotecas `tkinter` para interface gráfica e `scipy.optimize` para a solução matemática, este aplicativo permite definir funções objetivo e restrições de forma interativa e visualizar os resultados.

## Funcionalidades

- Entrada interativa para o número de variáveis de decisão e restrições.
- Definição da função objetivo e das restrições com interface amigável.
- Resolução de problemas de maximização utilizando o Método Simplex.
- Ajuste de recursos com análise de viabilidade baseada nos preços sombra.
- Mensagens informativas sobre resultados ou erros durante o processo.

## Requisitos

- Python 3.8 ou superior
- Bibliotecas Python:
  - `tkinter` (inclusa na instalação padrão do Python)
  - `scipy`

- A biblioteca python scipy pode ser instalada com o seguinte comando:

```sh
    pip install scipy
```

## Como Executar

1. Insira o número de variáveis de decisão e restrições na interface inicial e clique em Definir Problema.

2. Preencha os campos para a função objetivo e as restrições.

3. Clique em Resolver para calcular a solução ótima e visualizar o valor da função objetivo.

4. Utilize a funcionalidade de Ajuste de Recursos para aplicar alterações nas restrições e verificar os impactos na solução.

