import flatbuffers
import H3DData.ClockEvent
import H3DData.GammaEvent
import H3DData.H3DPacket
import H3DData.Interaction
import H3DData.MaskEvent
import H3DData.SyncEvent
import socket
import csv
import itertools
import statistics
from sklearn import preprocessing
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

X_data =[]
Y_data = []
Z_data =[]
E_data = []
dir=[[],[],[]]
angle=[]
d=[[],[],[]]
ERM= 511000
count=0

# Set IPv4 address of the detector publishing the data
HOST = '192.168.3.10'
PORT = 11503
ADDR = (HOST,PORT)
# Create socket connection -----------------------------------------------------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
# Read data from socket and parse -----------------------------------------------------
# Save the sound levels to a CSV file

count=0

def plot_heatmap(X, Y, Z):
    """
    Plot a heatmap with given X, Y, and Z lists.

    Parameters:
    X (list): List of X coordinates.
    Y (list): List of Y coordinates.
    Z (list): List of Z values.

    Returns:
    None
    """
    # Convert lists to numpy arrays
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    # Set up the figure and axis
    fig, ax = plt.subplots()

    # Create heatmap
    heatmap = ax.scatter(X, Y, c=Z, cmap='viridis')

    # Add color bar
    cbar = fig.colorbar(heatmap)
    cbar.set_label('Z')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Heatmap')

    # Show plot
    plt.show()

while True:
    packetSize = int.from_bytes(client.recv(4), byteorder='little', signed=True)
    

    buffer = b""
    while len(buffer) < packetSize:
        buffer += client.recv(packetSize - len(buffer))
    packetIn = H3DData.H3DPacket.H3DPacket.GetRootAsH3DPacket(buffer, 0)
    #print("Gamma events:", packetIn.GammaeventsLength(),end="\n")
    if (packetIn.GammaeventsLength() > 0):
        i=0
        
        while i<packetIn.GammaeventsLength():
            if packetIn.Gammaevents(i).InteractionsLength()==2:
                j=0
                while j<packetIn.Gammaevents(i).InteractionsLength():
                    X_data.append(packetIn.Gammaevents(i).Interactions(j).X())
                    Y_data.append(packetIn.Gammaevents(i).Interactions(j).Y())
                    Z_data.append(packetIn.Gammaevents(i).Interactions(j).Z())
                    E_data.append(packetIn.Gammaevents(i).Interactions(j).Energy())
                    
                    j+=1
                    count+=1
            i+=1
            
    print("Counts:",count,end="\r")
    if count>1000:
            E1=E_data[0::2]
            E2=E_data[1::2]

            E_gamma = [a + b for a, b in zip(E1, E2)]

            M_energy=statistics.mode(np.round((np.array(E_gamma) / 1000))*1000)

            angle=[]
            dir=[]
            h=0
            for i in range(0,len(E_data),2):
                d=[X_data[i]-X_data[i+1],Y_data[i]-Y_data[i+1],Z_data[i]-Z_data[i+1]]
                d=preprocessing.normalize([d])
                E0=E_data[i]+E_data[i+1]
                E1=E_data[i+1]
                if E0<400000:
                    d=-d
                    E1=E_data[i]
                if abs(1-(ERM*(1/E1-1/E0)))>1:
                    d=-d
                    E1=E_data[i]
                if abs(1-(ERM*(1/E1-1/E0)))<1:
                    ang=math.acos(1-(ERM*(1/E1-1/E0)))

                if abs(M_energy-E0)<0.03*M_energy:
                    angle.append(ang)
                    dir.append(d)
                    h=h+1

            dir=np.array(dir)                    

            j=0
            points=[]
            cones=[]
            for i in range(len(dir)):
                x=dir[i][0][0]
                y=dir[i][0][1]
                z=dir[i][0][2]
                B=np.arccos(z)
                g=np.arctan2(y,x)
                theta=angle[i]
                
                iter=0
                for t in np.arange(0.1,360,0.1):
                    if not angle[i]==0:  
                        x1=(np.sin(theta)*np.cos(B)*np.cos(g))*np.cos(t)+(np.sin(theta)*np.sin(g))*np.sin(t)-(np.cos(theta)*np.sin(B)*np.cos(g))
                        y1=-(np.sin(theta)*np.cos(B)*np.sin(g))*np.cos(t)+(np.sin(theta)*np.cos(g))*np.sin(t)+(np.cos(theta)*np.sin(B)*np.sin(g))
                        z1=(np.sin(theta)*np.sin(B))*np.cos(t)+np.cos(theta)*np.cos(B)
                        rho=np.arctan2(y1,x1)
                        phi=np.arccos(z1)
                        cones.append([x1,y1,z1])
                    iter=iter+1;               
            cones = np.round( (np.array(cones) * 15))/15
            Mu, idx = np.unique(cones, axis=0, return_inverse=True)
            Tally = np.bincount(idx)
            ixs = np.argsort(Tally)[::-1]
            Result = np.hstack([Mu[ixs], Tally[ixs][:, np.newaxis]])

            final_pos=[0,0,0]
            w=0
            Result[:,3]=Result[:,3]-statistics.mean(Result[:,3])
            for it in np.arange(1,10,1):
                x_pos=Result[it,0]
                y_pos=Result[it,1]
                z_pos=Result[it,2]
                Weight=Result[it,3]**2
                final_pos=final_pos+np.dot([x_pos,y_pos,z_pos],Weight);
                w=w+Weight
            final_pos=np.dot(final_pos,(1/w))
            
            rho = np.degrees(np.arctan2(Result[:,0], Result[:,1]))
            phi = np.degrees(np.arccos(Result[:,2]))
            num = Result[:,3]

            #plot_heatmap(phi, rho, num)
            final_pos = Result[0]
            pos = [np.degrees(final_pos[0]), np.degrees(final_pos[1])]
            print(pos)
            

            X_data =[]
            Y_data = []
            Z_data =[]
            E_data = []
            dir=[[],[],[]]
            angle=[]
            d=[[],[],[]]
            ERM= 511000
            count=0
f.close
                

