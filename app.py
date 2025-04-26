import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    """Função principal do aplicativo Streamlit"""
    # Configuração da página e título
    configurar_pagina()
    
    # Coletar parâmetros da interface
    params_iniciais = coletar_parametros_iniciais()
    params_choque = coletar_parametros_choque(params_iniciais)
    
    # Calcular equilíbrios
    Y_eq, i_eq = calcular_equilibrio(**params_iniciais)
    Y_eq_new, i_eq_new = calcular_equilibrio(
        **{**params_iniciais, 'G': params_choque['G_new'], 
           'T': params_choque['T_new'], 'M_supply': params_choque['M_new']}
    )
    
    # Gerar pontos para as curvas
    limites_y = determinar_limites_y(Y_eq, Y_eq_new)
    curvas_iniciais = gerar_curvas(**params_iniciais, **limites_y)
    curvas_choque = gerar_curvas(
        **{**params_iniciais, 'G': params_choque['G_new'], 
           'T': params_choque['T_new'], 'M_supply': params_choque['M_new']},
        **limites_y
    )
    
    # Exibir os gráficos
    exibir_graficos(curvas_iniciais, curvas_choque, Y_eq, i_eq, Y_eq_new, i_eq_new)
    
    # Mostrar resultados numéricos
    exibir_resultados(Y_eq, i_eq, Y_eq_new, i_eq_new)

def configurar_pagina():
    """Configura o título e descrição da página"""
    st.title("Bem vindo ao Modelo IS-LM Interativo")
    st.write("""
    Este aplicativo permite simular cenários macroeconômicos ajustando parâmetros de consumo, investimento, governo, impostos, moeda e preços.

- A curva **IS** representa o equilíbrio no mercado de bens (onde investimento = poupança).
- A curva **LM** representa o equilíbrio no mercado monetário (oferta de moeda = demanda por moeda).

Experimente alterar os parâmetros no menu lateral e observe como o equilíbrio (produto Y* e taxa de juros i*) muda em resposta a choques de políticas fiscais (G ou T) e monetárias (M).

**Fórmulas básicas do modelo:**""")
    
    # Exibição das fórmulas básicas do modelo IS-LM
    exibir_formulas()

def exibir_formulas():
    """Exibe as fórmulas do modelo IS-LM"""
    st.markdown("**Curva IS – Equilíbrio no Mercado de Bens:**")
    st.latex(r"C = C_0 + c\,(Y - T)")
    st.write(" Onde C = Consumo Total, \(C_0\) = Consumo autônomo, \(c\) = Propensão marginal a consumir, \(Y\) = Renda, \(T\) = Impostos")
    st.latex(r"I = I_0 - b\,i")
    st.write(" Onde I = Investimento Total, \(I_0\) = Investimento autônomo, \(b\) = Sensibilidade do investimento à taxa de juros \(i\)") 
    st.write("No equilíbrio da curva IS: \(Y = C + I + G + X - M\), ou seja, a demanda agregada iguala o produto \(Y\).")
    st.write( "Onde Y = Renda agregada, \(C\) = Consumo Total, \(I\) = Investimento Total, \(G\) = Gastos do governo, \(X\) = Exportações, \(M\) = Importações.")
    st.markdown("**Curva LM – Equilíbrio no Mercado Monetário:**")
    st.latex(r"L = L_0 + k\,Y - h\,i")
    st.write(" Onde L = Demanda por moeda, \(L_0\) = Demanda autônoma por moeda, \(k\) = Sensibilidade da demanda de moeda à renda \(Y\), \(h\) = Sensibilidade da demanda de moeda à taxa de juros \(i\)")
    st.write("No equilíbrio da curva LM: \(L = \frac{M}{P}\), onde \(M/P\) é a oferta real de moeda disponível no mercado monetário.")

    

def coletar_parametros_iniciais():
    """Coleta os parâmetros iniciais do modelo da interface"""
    st.sidebar.header("Parâmetros Iniciais do Modelo")
    
    # IS parameters
    C0 = st.sidebar.number_input("Consumo Autônomo (C0)", value=20.0, step=1.0)
    c = st.sidebar.slider("Propensão Marginal a Consumir (c)", min_value=0.0, max_value=1.0, value=0.8, step=0.05)
    I0 = st.sidebar.number_input("Investimento Autônomo (I0)", value=50.0, step=1.0)
    b = st.sidebar.number_input("Sensibilidade do Investimento à i (b)", value=10.0, step=1.0)
    G = st.sidebar.number_input("Gastos do Governo (G)", value=100.0, step=1.0)
    T = st.sidebar.number_input("Impostos (T)", value=50.0, step=1.0)
    X = st.sidebar.number_input("Exportações (X)", value=0.0, step=1.0)
    M_imp = st.sidebar.number_input("Importações (M)", value=0.0, step=1.0)

    # LM parameters
    st.sidebar.markdown("---")
    L0 = st.sidebar.number_input("Demanda por Moeda Autônoma (L0)", value=0.0, step=1.0)
    k = st.sidebar.number_input("Sensibilidade da Demanda de Moeda à Renda (k)", value=0.5, step=0.1)
    h = st.sidebar.number_input("Sensibilidade da Demanda de Moeda à Taxa de Juros (h)", value=10.0, step=1.0)
    M_supply = st.sidebar.number_input("Oferta de Moeda (M)", value=150.0, step=1.0)
    P = st.sidebar.number_input("Nível de Preços (P)", value=1.0, step=0.1)
    
    return {
        'C0': C0, 'c': c, 'I0': I0, 'b': b, 'G': G, 'T': T, 'X': X, 'M_imp': M_imp,
        'L0': L0, 'k': k, 'h': h, 'M_supply': M_supply, 'P': P
    }

def coletar_parametros_choque(params_iniciais):
    """Coleta os parâmetros de choque da interface"""
    st.sidebar.header("Parâmetros Após Choque")
    G_new = st.sidebar.number_input("Novo G (Gastos do Governo pós-choque)", value=float(params_iniciais['G']), step=1.0)
    T_new = st.sidebar.number_input("Novo T (Impostos pós-choque)", value=float(params_iniciais['T']), step=1.0)
    M_new = st.sidebar.number_input("Nova Oferta de Moeda (M pós-choque)", value=float(params_iniciais['M_supply']), step=1.0)
    
    return {'G_new': G_new, 'T_new': T_new, 'M_new': M_new}

def calcular_equilibrio(C0, c, I0, b, G, T, X, M_imp, L0, k, h, M_supply, P, **kwargs):
    """
    Calcula o equilíbrio IS-LM (Y* e i*) dado um conjunto de parâmetros.
    
    Retorna o par (Y*, i*) que satisfaz simultaneamente as equações IS e LM.
    Equações:
      IS: (1-c)*Y = C0 - c*T + I0 + G + X - M_imp - b*i
      LM: k*Y = L0 + h*i + (M_supply/P)  (rearranjado de L = M/P)
    """
    # Coeficientes e termos independentes das equações lineares:
    # IS: (1-c)*Y + b*i = C0 - c*T + I0 + G + X - M_imp
    A = C0 - c*T + I0 + G + X - M_imp  # termo autônomo da IS (demanda agregada autônoma)
    # LM: k*Y - h*i = M_supply/P - L0
    B = (M_supply / P) - L0           # diferença entre oferta real de moeda e demanda autônoma
    
    # Resolvendo o sistema linear:
    # (1-c)*Y + b*i = A  ...(1)
    # k*Y - h*i = B    ...(2)
    # Solução:
    det = (1 - c)*(-h) - (b * k)  # determinante do sistema 2x2
    if abs(det) < 1e-6:
        return None, None  # se determinante ~0, equilíbrio não é único (curvas paralelas ou sobrepostas)
    # Cramer's rule:
    Y_star = (A * (-h) - (b * B)) / det
    i_star = ((1 - c) * B - A * k) / det
    return Y_star, i_star

def determinar_limites_y(Y_eq, Y_eq_new):
    """Determina os limites de Y para o gráfico com base nos equilíbrios"""
    # Define Y_min e Y_max de forma abrangente se equilíbrio não definido
    Y_center = 0
    if Y_eq is not None:
        Y_center = Y_eq
    elif Y_eq_new is not None:
        Y_center = Y_eq_new
    
    if Y_center is None:
        Y_center = 100.0
        
    Y_min = max(0.0, Y_center * 0.5)
    Y_max = max(50.0, Y_center * 1.5)
    
    return {'Y_min': Y_min, 'Y_max': Y_max}

def gerar_curvas(C0, c, I0, b, G, T, X, M_imp, L0, k, h, M_supply, P, Y_min=None, Y_max=None, **kwargs):
    """
    Gera pontos das curvas IS e LM para plotagem.
    
    Retorna:
        Y_vals: Array de valores de Y
        i_is: Valores correspondentes de i na curva IS
        i_lm: Valores correspondentes de i na curva LM
    """
    # Gera um array de Y para traçar as curvas
    Y_vals = np.linspace(Y_min, Y_max, 200)
    
    # Calcula i da curva IS: isolando i da equação IS => b*i = C0 - c*T + I0 + G + X - M_imp - (1-c)*Y
    # Se b == 0, a curva IS é vertical (i não depende de Y); se c == 1, IS seria horizontal (caso extremo).
    if b != 0:
        i_is = (C0 - c*T + I0 + G + X - M_imp - (1 - c) * Y_vals) / b
    else:
        i_is = np.full_like(Y_vals, np.nan)  # não definida nesse formato (vertical)
        
    # Calcula i da curva LM: da equação LM => h*i = k*Y - (M/P - L0)
    if h != 0:
        i_lm = (k * Y_vals - ((M_supply / P) - L0)) / h
    else:
        i_lm = np.full_like(Y_vals, np.nan)  # LM vertical se h=0
        
    return Y_vals, i_is, i_lm

def exibir_graficos(curvas_iniciais, curvas_choque, Y_eq, i_eq, Y_eq_new, i_eq_new):
    """Cria e exibe os gráficos do modelo IS-LM"""
    Y_vals, i_is, i_lm = curvas_iniciais
    Y_vals2, i_is2, i_lm2 = curvas_choque
    
    # Criação dos gráficos usando Matplotlib
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Gráfico 1: Equilíbrio inicial
    plotar_equilibrio_inicial(ax1, Y_vals, i_is, i_lm, Y_eq, i_eq)
    
    # Gráfico 2: Após o choque (novas curvas)
    plotar_equilibrio_pos_choque(ax2, Y_vals, i_is, i_lm, Y_vals2, i_is2, i_lm2, Y_eq, i_eq, Y_eq_new, i_eq_new)

    # Ajuste de layout e exibição no Streamlit
    plt.tight_layout()
    st.pyplot(fig)

def plotar_equilibrio_inicial(ax, Y_vals, i_is, i_lm, Y_eq, i_eq):
    """Plota o gráfico de equilíbrio inicial"""
    ax.plot(Y_vals, i_is, label="Curva IS", color="blue")
    ax.plot(Y_vals, i_lm, label="Curva LM", color="green")
    
    if Y_eq is not None and i_eq is not None:
        ax.scatter(Y_eq, i_eq, color="red", zorder=5)
        ax.annotate(f"Equilíbrio\n(Y*={Y_eq:.1f}, i*={i_eq:.2f})", 
                     (Y_eq, i_eq), textcoords="offset points", xytext=(10, -15), color="red")
                     
    ax.set_xlabel("Produto (Y)")
    ax.set_ylabel("Taxa de Juros (i)")
    ax.set_title("Equilíbrio Inicial")
    ax.legend()
    ax.grid(True)

def plotar_equilibrio_pos_choque(ax, Y_vals, i_is, i_lm, Y_vals2, i_is2, i_lm2, Y_eq, i_eq, Y_eq_new, i_eq_new):
    """Plota o gráfico de equilíbrio após choque"""
    # Novas curvas
    ax.plot(Y_vals2, i_is2, label="Curva IS (novo)", color="blue", linestyle="-")
    ax.plot(Y_vals2, i_lm2, label="Curva LM (novo)", color="green", linestyle="-")
    
    # Curvas antigas em tracejado para referência
    ax.plot(Y_vals, i_is, label="IS (inicial)", color="blue", linestyle="--", alpha=0.5)
    ax.plot(Y_vals, i_lm, label="LM (inicial)", color="green", linestyle="--", alpha=0.5)
    
    # Marcar novos e antigos equilíbrios
    if Y_eq_new is not None and i_eq_new is not None:
        ax.scatter(Y_eq_new, i_eq_new, color="red", zorder=5)
        ax.annotate(f"Novo Equilíbrio\n(Y**={Y_eq_new:.1f}, i**={i_eq_new:.2f})",
                     (Y_eq_new, i_eq_new), textcoords="offset points", xytext=(10, -15), color="red")
                     
    if Y_eq is not None and i_eq is not None:
        ax.scatter(Y_eq, i_eq, color="orange", zorder=5)
        ax.annotate("Equilíbrio Inicial", (Y_eq, i_eq), textcoords="offset points", xytext=(10, 10), color="orange")
        
    ax.set_xlabel("Produto (Y)")
    ax.set_ylabel("Taxa de Juros (i)")
    ax.set_title("Após Choque de Política")
    ax.legend()
    ax.grid(True)

def exibir_resultados(Y_eq, i_eq, Y_eq_new, i_eq_new):
    """Exibe os resultados numéricos dos equilíbrios"""
    if Y_eq is not None and i_eq is not None and Y_eq_new is not None and i_eq_new is not None:
        st.markdown(f"**Equilíbrio inicial:** Y* = {Y_eq:.2f}, i* = {i_eq:.2f} &nbsp;&nbsp; | &nbsp;&nbsp; **Novo equilíbrio:** Y** = {Y_eq_new:.2f}, i** = {i_eq_new:.2f}")
    else:
        st.markdown("*(Parâmetros selecionados podem não produzir um equilíbrio único. Verifique as configurações.)*")

if __name__ == "__main__":
    main()