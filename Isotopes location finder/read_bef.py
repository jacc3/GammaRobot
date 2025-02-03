import os
import struct
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import csv

def read_bef(filedir):
    fid_path = os.path.join(filedir, 'AllEventsEu152.bef')
    listmodefile_path = os.path.join(filedir, 'AllEvents_listMode.csv')  # Change file extension to CSV

    if not os.path.exists(fid_path):
        print(f"File not found: {fid_path}")
        return

    with open(fid_path, 'rb') as fid, open(listmodefile_path, 'w', newline='') as csvfile:
        edges_e = np.arange(1001)
        hist2debef = np.zeros((len(edges_e), 5))
        
        totevt = 0
        bSkipWrongData = 0
        start_time = time.time()

        # Set up CSV writer
        csv_writer = csv.writer(csvfile)
        # Write header if needed
        csv_writer.writerow(['EventTime', 'NumPixels', 'Energy', 'ModuleID', 'X', 'Y', 'Z'])
        
        fid.seek(0, os.SEEK_END)
        fsize = fid.tell()
        fid.seek(0, os.SEEK_SET)

        while fid.tell() < fsize:
            cdatatype_data = fid.read(1)
            if len(cdatatype_data) == 0:
                break
                
            cdatatype = struct.unpack("b", cdatatype_data)[0]

            if cdatatype <= 0 and bSkipWrongData == 0:
                if cdatatype == 0:
                    try:
                        nFormatVersion = struct.unpack("I", fid.read(4))[0]
                        strIntro = fid.read(20)
                        
                        nLen = struct.unpack("H", fid.read(2))[0]
                        strFilename = fid.read(nLen)
                        
                        print(f'Format version = {nFormatVersion}')
                        print(f'  =>: {strIntro.decode().strip()}')
                        print(f'  =>: {strFilename.decode().strip()}')

                        nTimeStart = struct.unpack("I", fid.read(4))[0]
                        nTimeStartFraction = struct.unpack("I", fid.read(4))[0]
                        nFPGAStart = struct.unpack("I", fid.read(4))[0]
                        nFPGAStartFraction = struct.unpack("I", fid.read(4))[0]
                        cBEFEnergyOnly = struct.unpack("B", fid.read(1))[0]

                        if nFormatVersion >= 8:
                            cIndMode = struct.unpack("c", fid.read(1))[0]

                        nAdditionalHeaderLength = struct.unpack("I", fid.read(4))[0]

                        print(f'Computer Time: {nTimeStart} - {nTimeStartFraction}')
                        print(f'FPGA Time: {nFPGAStart} - {nFPGAStartFraction}')
                    except struct.error as e:
                        print("Error while unpacking header data:", e)
                        break

                elif cdatatype == -4:
                    try:
                        nLen = struct.unpack("H", fid.read(2))[0]
                        strDeviceID = fid.read(nLen)
                        print(f"Device ID: {strDeviceID.decode().strip()}")
                    except struct.error as e:
                        print("Error while unpacking Device ID:", e)
                        break

                elif cdatatype == -100:
                    try:
                        unused_data_bytes = fid.read(12)
                        if len(unused_data_bytes) == 12:  # Ensure we read enough bytes
                            dwUnusded = struct.unpack("3I", unused_data_bytes)
                        else:
                            print("Error: Not enough data for unused data")
                            break
                    except struct.error as e:
                        print("Error while unpacking unused data:", e)
                        break

                else:
                    print(f"Unknown data type {cdatatype}")
                    try:
                        dwUnusded0 = struct.unpack("I", fid.read(4))[0]
                        dwUnusded1 = struct.unpack("I", fid.read(4))[0]
                        dwUnusded2 = struct.unpack("I", fid.read(4))[0]
                        print(f"Wrong Data: {dwUnusded0} {dwUnusded1} {dwUnusded2}")
                    except struct.error as e:
                        print("Error while unpacking wrong data:", e)
                        break

            else:
                if 0 < cdatatype <= 121:
                    nEnergy = np.zeros(121)
                    nModuleID = np.zeros(121)
                    nX = np.zeros(121)
                    nY = np.zeros(121)
                    nZ = np.zeros(121)

                    try:
                        npix = 1
                        if nFormatVersion < 7 and cBEFEnergyOnly == 1:
                            nEnergy[0] = struct.unpack("I", fid.read(4))[0]
                        else:
                            npix = cdatatype
                            for ii in range(cdatatype):
                                if cBEFEnergyOnly == 1 and (nFormatVersion >= 8 or (nFormatVersion == 7 and cIndMode == 1)):
                                    nModuleID[ii] = struct.unpack("c", fid.read(1))[0]
                                    
                                if nFormatVersion <= 5:
                                    nEnergy[ii] = struct.unpack("H", fid.read(2))[0]
                                else:
                                    nEnergy[ii] = struct.unpack("I", fid.read(4))[0]
                        
                                if cBEFEnergyOnly == 0:
                                    nX[ii] = struct.unpack("h", fid.read(2))[0]
                                    nY[ii] = struct.unpack("h", fid.read(2))[0]
                                    nZ[ii] = struct.unpack("h", fid.read(2))[0]

                        nEventTime = struct.unpack("I", fid.read(4))[0]
                        dwLiveTime = struct.unpack("I", fid.read(4))[0]

                    except struct.error as e:
                        print("Error while unpacking event data:", e)
                        break
    
                    totEnergy = np.sum(nEnergy) / (1000 if nFormatVersion > 5 else 10)
             
                    idxe = np.argmax(edges_e > totEnergy)
                    
                    if npix <= 4:
                        hist2debef[idxe, npix] += 1
                    else:
                        hist2debef[idxe, 4] += 1
                    
                    for i in range(npix):
                        row = [int(nEventTime), int(npix), int(nEnergy[i]), int(nModuleID[i]), nX[i], nY[i], nZ[i]]
                        csv_writer.writerow(row)

                else:
                    bSkipWrongData = 1

            totevt += 1
            if totevt % 1e6 == 0:
                curtm = time.time() - start_time
                fpos = fid.tell()
                print(f'--: Elapsed Time: {curtm:.1f} seconds, Total Time: {curtm / fpos * fsize:.1f} seconds')

        np.save(os.path.join(filedir, 'befspec.npy'), hist2debef)

    plt.plot(hist2debef)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_bef.py <file_directory>")
    else:
        file_directory = sys.argv[1]
        read_bef(file_directory)
