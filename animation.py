import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib.cm as cm

interval = 30
show_trail = False
trail_width = 1 
save_to_file = True
limit=20             
dpi = 150 


file_out='particles_50'


with open('simulation_data_particles.txt', "r") as f:
    data_str = f.read()


frames_data = list()


for frame_data_str in data_str.split("\n"):
    
    frame_data = list()


    for p_pos_str in frame_data_str.split("\t"):
        
        if p_pos_str!='':
            frame_data.append(float(p_pos_str))

    
    frames_data.append(frame_data)




npart = int(len(frames_data[0])/4)



fig, ax = plt.subplots()


ax.set_xlim(0, limit)
ax.set_ylim(0, limit)





#print(frames_data[1])

part_points = list()
p_trails = list()


for i in range(npart):

    x= frames_data[0][4*i]
    y=frames_data[0][4*i+1]
    q=frames_data[0][4*i+2]
    R=frames_data[0][4*i+3]

    #p_point, = ax.plot(x, y, "o", markersize=10)
    if q>0:
        part_point = Circle((x, y), R, color='r')
    elif q<0:
        part_point = Circle((x, y), R, color='b')
    else:
        part_point = Circle((x, y), R, color='gray')

    ax.add_artist(part_point)
    part_points.append(part_point)

    
    if show_trail:
        p_trail, = ax.plot(
                x, y, "-", linewidth=trail_width)
        p_trails.append(p_trail)
 

def update(j_frame, frames_data, part_points, p_trails, show_trail):
    
    for i in range(npart):
        x= frames_data[j_frame][4*i]
        y= frames_data[j_frame][4*i+1]
        q= frames_data[j_frame][4*i+2]
        R= frames_data[j_frame][4*i+3]

        part_points[i].center = (x, y)
        part_points[i].radius = R
        if q>0:
            part_points[i].set_color('r')
        elif q<0:
            part_points[i].set_color('b')
        else:
            part_points[i].set_color('gray')

        if show_trail:
            xs_old, ys_old = p_trails[i].get_data()
            xs_new = np.append(xs_old, x)
            ys_new = np.append(ys_old, y)

            p_trails[i].set_data(xs_new, ys_new)

    return part_points + p_trails

def init_anim():
    
    if show_trail:
        for j_p in range(npart):
            p_trails[j_p].set_data(list(), list())

    return part_points + p_trails


nframes = len(frames_data)

if nframes > 1:
    # Info FuncAnimation: https://matplotlib.org/stable/api/animation_api.html
    animation = FuncAnimation(
            fig, update, init_func=init_anim,
            fargs=(frames_data, part_points, p_trails, show_trail),
            frames=len(frames_data), blit=True, interval=interval)

    
    if save_to_file:
        animation.save("{}.gif".format(file_out), dpi=dpi)
    else:
        plt.show()

else:
    
    if save_to_file:
        fig.savefig("{}.pdf".format(file_out))
    else:
        plt.show()
