% function read_bef(filename)
% filedir = 'I:\M400\20240515-200531_0cm';
% filedir = 'I:\M400\20240605-165232_20240605_cs137_alone_30_min';
filedir = 'C:\Users\Jacob\Desktop\m400';

fid = fopen(strcat(filedir, '\AllEventsEu152.bef'));
listmodefile = fopen(strcat(filedir, '\AllEvents_listMode.txt'), 'w');

if fid < 0
    return;
end

if listmodefile < 0
    return;
end

fseek(fid, 0, 'eof');
fsize = ftell(fid);
fseek(fid, 0, 'bof');

edges_e = 0:1000;
hist2debef = zeros(length(edges_e), 5);

totevt = 0;
bSkipWrongData = 0;
tic;
while (~feof(fid))
    [cdatatype, nread] = fread(fid, 1, "int8");
    if nread <= 0; break; end

    if cdatatype <= 0 && bSkipWrongData == 0
        if cdatatype == 0
            nFormatVersion = fread(fid, 1, "uint32");
            strIntro = fread(fid, 20, 'char');
            
            nLen = fread(fid, 1, 'uint16');
            strFilename = fread(fid, nLen, 'char');

            fprintf('Format version = %d\n', nFormatVersion);
            fprintf('  =>: %s\n', strIntro);
            fprintf('  =>: %s\n', strFilename);

            nTimeStart = fread(fid, 1, 'uint32');
            nTimeStartFraction = fread(fid, 1, 'uint32');
            nFPGAStart = fread(fid, 1, 'uint32');
            nFPGAStartFraction = fread(fid, 1, 'uint32');
            cBEFEnergyOnly = fread(fid, 1, 'uint8');
            if nFormatVersion >=8
                cIndMode = fread(fid, 1, 'char');
            end
            nAdditionalHeaderLength = fread(fid, 1, 'uint32');

            fprintf('Computer Time: %d - %d\n', nTimeStart, nTimeStartFraction);
            fprintf('FPGA Time: %d - %d\n', nFPGAStart, nFPGAStartFraction);

        elseif cdatatype == -4
            nLen = fread(fid, 1, 'uint16');
            strDeviceID = fread(fid, nLen, 'uint8');
            fprintf("Device ID: %s\n", strDeviceID);

        elseif cdatatype == -100
            dwUnusded = fread(fid, 3, 'uint32');
        else
            fprintf("Unknown data type %d\n", cdatatype);
            dwUnusded0 = fread(fid, 1, 'uint32');
            dwUnusded1 = fread(fid, 1, 'uint32');
            dwUnusded2 = fread(fid, 1, 'uint32');
            fprintf("Wrong Data:%d %d %d\n", dwUnusded0, dwUnusded1, dwUnusded2);
        end
    else
        if cdatatype > 0 && cdatatype <= 121

            nEnergy = zeros(121, 1);
            nModuleID = zeros(121, 1);
            nX = zeros(121, 1);
            nY = zeros(121, 1);
            nZ = zeros(121, 1);
    
            npix = 1;
            if nFormatVersion<7 && cBEFEnergyOnly==1
                nEnergy(1) = fread(fid, 1, 'uint32');
            else
                npix = cdatatype;
                for ii=1:cdatatype
                    if cBEFEnergyOnly==1 && (nFormatVersion >= 8 || (nFormatVersion == 7 && cIndMode == 1))
                        nModuleID(ii) = fread(fid, 1, 'char');
                    end
    
                    if nFormatVersion <= 5
                        nEnergy(ii) = fread(fid, 1, 'uint16');
                    else
                        nEnergy(ii) = fread(fid, 1, 'uint32');
                    end
                    
                    if cBEFEnergyOnly==0
                        nX(ii) = fread(fid, 1, 'short');
                        nY(ii) = fread(fid, 1, 'short');
                        nZ(ii) = fread(fid, 1, 'short');
                    end
                end
            end

            nEventTime = fread(fid, 1, 'uint32');
            dwLiveTime = fread(fid, 1, 'uint32');
    
            if(nFormatVersion <= 5)
                totEnergy = sum(nEnergy)/10;
            else
                totEnergy = sum(nEnergy)/1000;
            end
             
            % user code start here
            [~, idxe] = max(edges_e > totEnergy);
            
            if npix <= 4
                hist2debef(idxe, npix) = hist2debef(idxe, npix) + 1;
            else
                hist2debef(idxe, 5) = hist2debef(idxe, 5) + 1;
            end

            % user code end here

            for i = 1:npix
                newLine = sprintf('%d %10d %10d %10d %10.2f %10.2f %10.2f\n', int32(nEventTime), int32(npix), int32(nEnergy(i)), int32(nModuleID(i)), nX(i), nY(i), nZ(i));
                fprintf(listmodefile, newLine);
            end

        else
            bSkipWrongData = 1;
        end
    end

    totevt = totevt + 1;
    if mod(totevt, 1e6) == 0
        curtm = toc;
        fpos = ftell(fid);
        fprintf('--: Elasped Time: %.1f seconds, Total Time: %.1f seconds\n', curtm, curtm / fpos * fsize);
    end
end
toc;

fclose all;

save(sprintf('%s\\befspec.mat', filedir), 'hist2debef');

%%
plot(hist2debef)