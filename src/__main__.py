import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
import time

from config import Config
from particle import Particle
from physics import (
    start,
    calculate_density,
    create_pressure,
    calculate_viscosity,
)

(
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
) = Config().return_config()


def update(particles: list[Particle], dam: bool) -> list[Particle]:
    """
    Calcula um passo da simulação
    """
    # Atualiza o estado das particulas (aplica as forças, reseta os valores, etc.)
    for particle in particles:
        particle.update_state(dam)

    # Calcula a densidade
    calculate_density(particles)

    # Calcula a pressão
    for particle in particles:
        particle.calculate_pressure()

    # Aplica a força de pressão
    create_pressure(particles)

    # Aplica a força de viscosidade
    calculate_viscosity(particles)

    return particles


# Configuração do matplotlib
fig = plt.figure()
axes = fig.add_subplot(xlim=(-SIM_W, SIM_W), ylim=(0, SIM_W))
(POINTS,) = axes.plot([], [], "bo", ms=20)

simulation_state = start(-SIM_W, DAM, BOTTOM, 0.03, N)

frame = 0

dam_built = True

# Função de Animação
def animate(i: int):
    """
    Anima a simulação no matplotlib

    Args:
        i: número de frames

    Returns:
        points: os pontos para serem plotados
    """
    global simulation_state, frame, dam_built
    if frame == 10:  # Quebra a barreira no frame 10
        print("Breaking the dam")
        dam_built = False
    simulation_state = update(simulation_state, dam_built)
    # Cria um array com as coordenadas x e y das particulas
    visual = np.array(
        [
            [particle.visual_x_pos, particle.visual_y_pos]
            for particle in simulation_state
        ]
    )
    POINTS.set_data(visual[:, 0], visual[:, 1])  # Atualiza a posição das particulas
    frame += 1
    return (POINTS,)

start_time = time.time()

# Inicia e salva a animação
ani = animation.FuncAnimation(fig, animate, frames=300, interval=10, blit=True)
ani.save('animation.gif', writer='pillow')

end_time = time.time()
print(f'Tempo de execução: {end_time - start_time:.6f}')