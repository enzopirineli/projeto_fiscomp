"""Arquivo de configuração definindo os parâmetros da simulação."""

# Parâmetros da simulação
N = 250  # Número de partículas
SIM_W = 0.5  # Largura do espaço de simulação
BOTTOM = 0  # Nível do solo na simulação
DAM = -0.3  # Posição da barragem, o espaço de simulação é entre -0.5 e 0.5
DAM_BREAK = 200  # Número de frames antes que a barragem quebre

# Parâmetros físicos
G = 0.02 * 0.25  # Aceleração da gravidade
SPACING = 0.08  # Espaçamento entre partículas, usado para calcular a pressão
K = SPACING / 1000.0  # Fator de pressão
K_NEAR = K * 10  # Fator de pressão próxima, pressão quando as partículas estão próximas uma da outra
# Densidade padrão, será comparada à densidade local para calcular a pressão
REST_DENSITY = 3.0
# Raio de vizinhança, se a distância entre duas partículas for menor que R, elas são vizinhas
R = SPACING * 1.25
SIGMA = 0.2  # Fator de viscosidade
MAX_VEL = 2.0  # Velocidade máxima das partículas, usada para evitar instabilidade
# Fator de restrição de paredes, quanto mais as partículas são empurradas para longe das paredes da simulação
WALL_DAMP = 0.05
VEL_DAMP = 0.5  # Fator de redução da velocidade quando as partículas ultrapassam MAX_VEL


class Config:
    """Contém os parâmetros da simulação e os parâmetros para a física."""

    def __init__(self):
        return None

    def return_config(self):
        """Retorna os parâmetros da simulação e os parâmetros para a física."""
        return (
            N,
            SIM_W,
            BOTTOM,
            DAM,
            DAM_BREAK,
            G,
            SPACING,
            K,
            K_NEAR,
            REST_DENSITY,
            R,
            SIGMA,
            MAX_VEL,
            WALL_DAMP,
            VEL_DAMP,
        )
