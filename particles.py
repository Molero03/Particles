import numpy as np
import matplotlib.pyplot as plt
from numba import njit

#particles


N=100
L=20

m=np.zeros(N)
R=np.zeros(N)

dt = 0.01
nsteps =  12000 



xp=np.zeros((N,3))
vp=np.zeros((N,2))
T=np.zeros(nsteps)

nr=50
nb=N-nr
for i in range(0,N):
    xp[i,0]=np.random.uniform(0.3,L-0.3)
    xp[i,1]=np.random.uniform(0.3,L-0.3)
    m[i]=1.0
    R[i]=5*2.5/65
    if i<nb:
        xp[i,2]=-1
    else:
        xp[i,2]=1

@njit
def fuerzas(xp,m):
    dim=len(m)
    f=np.zeros((dim,2))
    a=np.zeros((dim,2))
    for i in range(0,dim):
        for j in range(i+1,dim):
            dx=xp[i,0]-xp[j,0]
            dy=xp[i,1]-xp[j,1]
            r2=dx**2+dy**2
            fx=xp[i,2]*xp[j,2]/r2*dx/np.sqrt(r2)
            fy=xp[i,2]*xp[j,2]/r2*dy/np.sqrt(r2)
            f[i,0]=f[i,0] + fx
            f[i,1]=f[i,1]+ fy
            f[j,0]=f[j,0] - fx
            f[j,1]=f[j,1] - fy

        a[i,0]=f[i,0]/m[i]
        a[i,1]=f[i,1]/m[i]

    
    return a





def update(xp, vp,m, dt=dt):
    
    dim=len(m)
    # Update positions and velocities
    vaux = np.zeros((dim, 2))
    xpnew = np.zeros((dim, 3))
    vpnew = np.zeros((dim, 2))

    vaux[:, 0] = vp[:, 0] + fuerzas(xp,m)[:, 0] * dt / 2
    vaux[:, 1] = vp[:, 1] + fuerzas(xp,m)[:, 1] * dt / 2

    xpnew[:, 0] = xp[:, 0] + vaux[:, 0] * dt
    xpnew[:, 1] = xp[:, 1] + vaux[:, 1] * dt
    xpnew[:, 2] = xp[:, 2]



    vpnew[:, 0] = vp[:, 0] + fuerzas(xpnew,m)[:, 0] * dt / 2
    vpnew[:, 1] = vp[:, 1] + fuerzas(xpnew,m)[:, 1] * dt / 2

    for i in range(0,dim):
        if xpnew[i,0] - R[i]<0.1 and vpnew[i,0]<0:
            vpnew[i,0]=abs(vpnew[i,0])
        if xpnew[i,0]+ R[i]>L-0.1 and vpnew[i,0]>0:
            vpnew[i,0]=-abs(vpnew[i,0])
        if xpnew[i,1]- R[i]<0.1 and vpnew[i,1]<0:
            vpnew[i,1]=abs(vpnew[i,1])
        if xpnew[i,1]+ R[i]>L-0.1 and vpnew[i,1]>0:
            vpnew[i,1]=-abs(vpnew[i,1])
    
    return xpnew, vpnew

def colision(xp,vp, R, m, deleted_part):
    dim=len(R)
    colisions=0
    detect=np.zeros((dim,2), dtype=np.int16)

    for i in range(dim):
        for j in range(i+1, dim):
            d2=(xp[i,0]-xp[j,0])**2 + (xp[i,1]-xp[j,1])**2

            if np.sqrt(d2)<=0.95*(R[i] + R[j]):
                detect[colisions,0]=i
                detect[colisions,1]=j
                colisions=colisions+1
    
    
                
    if colisions!=0:
        # when a particle is deleted its index in deleted_part is updated to 1
        # the for must decrease
        for i in range(colisions-1, -1, -1):
            elim=detect[colisions,0]
            
            deleted_part[original_label(elim, deleted_part)]=1
        
        for i in range(colisions):
            a=detect[i,0]
            b=detect[i,1]
            vp[b-i,0]= (m[a-i]*vp[a-i,0] + m[b-i]*vp[b-i,0])/(m[a-i]+m[b-i])
            vp[b-i,1]= (m[a-i]*vp[a-i,1] + m[b-i]*vp[b-i,1])/(m[a-i]+m[b-i])
            R[b-i]=R[b-i]*((m[a-i]+m[b-i])/m[b-i])**(1/3)
            m[b-i]=m[a-i] + m[b-i]
            xp[b-i,2]=xp[a-i,2] + xp[b-i,2]

            xp[b-i,0]=(m[b-i]*xp[b-i,0] + m[a-i]*xp[a-i,0])/(m[b-i] + m[a-i])
            xp[b-i,1]=(m[b-i]*xp[b-i,1] + m[a-i]*xp[a-i,1])/(m[b-i] + m[a-i])

            xp= np.delete(xp, a-i,0)
            vp= np.delete(vp, a-i,0)
            R= np.delete(R, a-i,0)
            m= np.delete(m, a-i,0)

    return xp, vp, R, m, deleted_part


#with this function you can recover the original index from the deleted particles
# list and the current index
@njit
def original_label(x, deleted_part):

    for k in range(N):
        if x>=k:
            x=x+deleted_part[k]
        else:
            return x
    return x


deleted_part=np.zeros(N, dtype=np.int8)


with open('simulation_data_particles.txt', 'w') as f:

    #structure x0   y0   q0   R0    x1  etc
    for i in range(N):
        for j in range(3):
            f.write(str(float(xp[i,j])) + '\t')
        
        if i!=N-1:
            f.write(str(float(R[i])) + '\t')
        else: 
            f.write(str(float(R[i])) + '\n')


    for i in range(1,nsteps):
    
        xp, vp= update(xp, vp, m, dt)

        xp, vp, R, m, deleted_part= colision(xp,vp,R,m, deleted_part)


        if i%5==0:
            dim=len(R)
            original_labels=np.zeros(dim, dtype=np.int8)
            for j in range(dim):
                original_labels[j]=original_label(j, deleted_part)
            # write on the file the required data of each particle
            # if a particle has been deleted write 0.0 for all its values
            # we can maintain the structure of the file by saving the data
            # of each particle in its original position (with the original labels array)
            # this array gives the original index of each particle that is still present
            # original_labels[j] is the original index of the particle with current index j
            # if deleted_part[k] is 1 the particle with original index k has been deleted
            for j in range(N):
                if deleted_part[j]>0:
                    for j in range(3):
                        f.write(str(0.0) + '\t')
        
                    if i!=N-1:
                        f.write(str(0.0) + '\t')
                    else: 
                        f.write(str(0.0) + '\n')
                else:
                    a=np.where(original_labels==j)

                    for k in range(3):
                        f.write(str(float(xp[a,k])) + '\t')
        
                    if original_labels[a]!=N-1:
                        f.write(str(float(R[a])) + '\t')
                    else: 
                        f.write(str(float(R[a])) + '\n')



        T[i]=np.mean(m[:]*(vp[:,0]**2 + vp[:,1]**2))



plt.xlim(0, nsteps+50)
plt.xlabel('steps', fontsize=15)
plt.ylabel('Temperature', fontsize=15)
plt.plot(np.arange(nsteps), T, color='r')
plt.show()

        





