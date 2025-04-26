
# Modelo IS-LM Interativo

## 📚 Descrição do Projeto

Este trabalho está sendo desenvolvido como parte do 1º Desafio EconoPy: Modelo IS-LM em Python, no âmbito do bacharelado em Ciências Econômicas na Pontifícia Universidade Católica de Minas Gerais (PUC-MG), sob orientação dos professores Prof. Marcelo Mendonça e Profa. Paola Faria Lucas de Sousa.

O **Modelo IS-LM Interativo** é uma aplicação web desenvolvida em Python com Streamlit que permite explorar, de forma visual e dinâmica, os efeitos de políticas fiscais e monetárias no equilíbrio macroeconômico. 

O modelo IS-LM é fundamental na macroeconomia keynesiana para analisar a interação entre o mercado de bens (curva IS - Investment-Savings) e o mercado monetário (curva LM - Liquidity-Money), determinando o equilíbrio simultâneo de produto e taxa de juros.



## ⚙️ Funcionalidades Implementadas
- **Parâmetros customizáveis:** Ajuste consumo autônomo, propensão a consumir, investimento, gastos do governo, impostos, exportações, importações, demanda/oferta de moeda e nível de preços.  

- **Visualização antes e depois:** Gráficos lado a lado mostram o equilíbrio inicial e o deslocamento das curvas IS-LM após choques econômicos.  

- **Ponto de equilíbrio destacado:** Valores de Y* (produto) e i* (taxa de juros) são calculados e exibidos visualmente no gráfico e numericamente abaixo.

- **Interface intuitiva:** Sliders e campos numéricos na barra lateral, com instruções embutidas para reforçar o embasamento teórico.

### 🗂️ Estrutura do Repositório
```
├── app.py ← código principal do Streamlit
├── requirements.txt ← dependências do projeto
├── README.md ← esta descrição e instruções gerais
└── docs/ ← guia do usuário (professor e estudante)
├── manual_professor.pdf
└── screenshots/
```

### 🚀 Como executar

1. **Clone este repositório**  
2. **Crie e ative um ambiente virtual:**
   ```
   bash
   
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   
   ```

3. **Instale dependências:**

    ```
    bash
    
    pip install -r requirements.txt
    ```
4. **Execute o app:**
    ```
    bash

    streamlit run app.py
    ```


## 🛠️ Sobre a Implementação

O código foi estruturado de forma modular para facilitar a compreensão e manutenção. As principais funções:

- Cálculo do equilíbrio IS-LM usando sistema de equações lineares
- Geração de curvas para visualização gráfica
- Interface de usuário interativa com Streamlit
- Visualização de resultados antes e após choques de política

 
 
 **✨ Planos Futuros (pós-entrega)**
- [ ] Análise de sensibilidade dos parâmetros (heatmaps)
- [ ] Integraão com dados econômicos reais (dowload de dados BACEN ou FRED)
- [ ] Implementaão do modelo Mundell-Fleming (economia aberta)
- [ ] Simulação dinâmica por períodos

