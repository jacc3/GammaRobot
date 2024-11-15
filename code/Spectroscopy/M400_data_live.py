import flatbuffers
import H3DData.ClockEvent
import H3DData.GammaEvent
import H3DData.H3DPacket
import H3DData.Interaction
import H3DData.MaskEvent
import H3DData.SyncEvent
import socket
import csv
# Set IPv4 address of the detector publishing the data
HOST = '192.168.3.10'
PORT = 11503
ADDR = (HOST,PORT)
# Create socket connection -----------------------------------------------------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
# Read data from socket and parse -----------------------------------------------------
# Save the sound levels to a CSV file
csv_file = 'M400Data.csv'
count=0

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['X','Y','Z','Energy'])
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
                if packetIn.Gammaevents(i).InteractionsLength()==1:
                    j=0
                    while j<packetIn.Gammaevents(i).InteractionsLength():
                        X= packetIn.Gammaevents(i).Interactions(j).X()
                        Y= packetIn.Gammaevents(i).Interactions(j).Y()
                        Z= packetIn.Gammaevents(i).Interactions(j).Z()
                        Energy= packetIn.Gammaevents(i).Interactions(j).Energy()
                        writer.writerow([X,Y,Z,Energy])
                        j+=1
                        count+=1
                i+=1
                
        print("Counts:",count,end="\r")
f.close
                    

