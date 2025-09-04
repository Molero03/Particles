# Particles

The project consists of a Python program that simulates the dynamics of N charged particles (nr particles positive charge and nb with negative charge) that are trapped in a box. The particles can have inelastic collisions in which the charge, mass and density is conserved. The time evolution of the particles is obtain using the Verlet algorithm, which obtains the positions and velocities of the particles after a set time step. Then, the information of each particle is stored in a .txt file. At the end of the process, a plot of the "temperature" (proportional to the mean kinetic energy of the system) is displayed. <br />

In order to visualize the data, you can use the program "animation.py". <br /> 

# # Some examples

100 particles with net charge equal to 0.

![Particles_50](https://github.com/Molero03/Particles/blob/main/particles_50.gif)


100 particles with net charge equal to 40.

![Particles_70](https://github.com/Molero03/Particles/blob/main/particles_70.gif)



100 particles with net charge equal to 90.

![Particles_95](https://github.com/Molero03/Particles/blob/main/particles_95.gif)


Note: In the animation, the red particles have positive charge and the blue particles a negative charge. The grey particles are neutral and its only interaction is through random collisions with other particles.
