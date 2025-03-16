def isolar_variaveis(matriz_aumentada):
    """Isola variáveis para Jacobi: retorna matriz de coeficientes e termos independentes."""
    n = len(matriz_aumentada)
    matriz_coef_isolada = [[0.0] * n for _ in range(n)]
    termos_indep_isolados = [0.0] * n

    for i in range(n):
        elem_diagonal = matriz_aumentada[i][i]  # Elemento da diagonal principal
        if elem_diagonal == 0:
            print(f"Erro: Elemento diagonal zero na linha {i}. Método de Jacobi pode falhar.")
            continue

        termos_indep_isolados[i] = matriz_aumentada[i][-1] / elem_diagonal  # Isola termo constante
        for j in range(n):
            matriz_coef_isolada[i][j] = -matriz_aumentada[i][j] / elem_diagonal if i != j else 0.0  # Zera diagonal

    return matriz_coef_isolada, termos_indep_isolados


def aproximar_resultado(matriz_coef_isolada, termos_indep_isolados, aprox_anteriores):
    """Calcula nova aproximação usando valores da iteração anterior."""
    n = len(matriz_coef_isolada)
    aprox_novas = [0.0] * n
    for i in range(n):
        aprox_novas[i] = termos_indep_isolados[i]  # Inicializa com termo constante
        for j in range(n):
            if i != j: # Ignora posição diagonal do sistema
                aprox_novas[i] += matriz_coef_isolada[i][j] * aprox_anteriores[j]
    return aprox_novas


def comparar_tolerancia(aprox_atual, aprox_anterior, tolerancia):
    """Verifica convergência entre iterações, considerando a norma-infinito."""
    verificacoes = []
    for i in range(len(aprox_atual)):
        try:  # Evita divisão por zero para valores próximos de zero
            diferenca_relativa = abs(aprox_atual[i] - aprox_anterior[i]) / abs(aprox_atual[i])
            verificacoes.append(diferenca_relativa < tolerancia)
        except ZeroDivisionError:
            verificacoes.append(abs(aprox_atual[i] - aprox_anterior[i]) < tolerancia)
    return all(verificacoes)  # Todos elementos devem satisfazer a tolerância


def jacobi(matriz_aumentada, num_iteracoes, tolerancia):
    """Implementa método iterativo de Jacobi para sistemas lineares."""
    matriz_coef_isolada, termos_indep_isolados = isolar_variaveis(matriz_aumentada)
    aprox_atual = [0.0] * len(matriz_aumentada)  # Chute inicial [0,0,...0]

    for i in range(num_iteracoes):
        aprox_anterior = list(aprox_atual)
        aprox_atual = aproximar_resultado(matriz_coef_isolada, termos_indep_isolados, aprox_anterior)
        if comparar_tolerancia(aprox_atual, aprox_anterior, tolerancia):
            print(f"Convergiu na iteração {i}")
            return aprox_atual  # Convergência antecipada
    print("Limite de iterações atingido")
    return aprox_atual  # Retorna após máximo de iterações ser atingido


def imprimir_lista(lista):
    """Formata saída numérica com 4 casas decimais."""
    for i in range(len(lista)):
        print(f"{lista[i]:.4f}", end=" ") # Imprime até a quarta casa decimal
    print("\n")


def imprimir_matriz(matriz):
    """Exibe matriz aumentada do sistema de forma legível."""
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f"{matriz[i][j]:>6}", end=" ")
        print()

def main():

    # Exercicio 1

    sistema1 = [
    [10, -1, 2, 0, 6],
    [-1, 11, -1, 3, 25],
    [2, -1, 10, -1, -11],
    [0, 3, -1, 8, 15]
    ]
    tolerancia = 1e-3

    print("Sistema:")
    imprimir_matriz(sistema1)

    print("Resultado com Método de Jacobi:")
    imprimir_lista(jacobi(sistema1, 10, tolerancia))


if __name__ == '__main__':
    main()