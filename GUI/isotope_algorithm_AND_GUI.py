import os
import xmlwrapper
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, savgol_filter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ttkthemes import ThemedTk

# Existing code (unchanged)
class Spectra:
    def __init__(self, file, counts, compressed):
        self.iso_name = file[file.rindex('/')+1:file.rindex('_')]
        if compressed:
            self.counts = expand_zeros(counts)
        else:
            self.counts = [float(el) for el in counts.split(" ")[:-1]]
        self.wdt_arr = np.array([max(i,2) for i in np.arange(0,len(self.counts),1)*0.005])
        self.height_vec = find_height(self.counts)
        self.prom = 0.01*max(self.counts)

def expand_zeros(counts):
    counts = counts.split()
    counts = [int(el) for el in counts]
    zeros = []
    for i in range(0,len(counts)):
        count = counts[i]
        if count == 0:
            zeros.append([i, counts[i+1]])     
    for i in range(len(zeros)-1,-1,-1):
        ind,num = zeros[i]
        counts = counts[0:ind] + [0]*num + counts[ind+2:]
    return counts   

def find_height(counts):
    std_dev = []
    for i in range(1,len(counts)-1):
        std_dev.append(np.sqrt(counts[i-1] + 4*counts[i] + counts[i+1]))
    std_dev.append(0)
    std_dev.insert(0,0)  
    counts_filtered = savgol_filter(counts, 50, 2)
    height = np.array([int(max(std_dev[i]+0.98*counts_filtered[i],1)) for i in range(len(std_dev))])
    return height 

def determine_name(iso_name):
    iso_name = iso_name.lower()
    if "heu" in iso_name:
        iso_name = iso_name.replace("heu","u235u-238")
    elif "du" in iso_name:
        iso_name = iso_name.replace("du","u235u-238")
    elif "wgpu" in iso_name:
        iso_name = iso_name.replace("wgpu","pu239")
    old_nm = iso_name
    for x in range(len(old_nm)):
        if iso_name[x].isalpha() and iso_name[x+1].isdigit():
            iso_name = iso_name[:x+1] + '-' + iso_name[x+1:]
        elif iso_name[x].isdigit() and iso_name[x+1].isalpha():
            iso_name = iso_name[:x+1] + ',' + iso_name[x+1:]
    if "tc-99" in iso_name:
        iso_name += "m"
    return iso_name.split(',')

def isotope_peaks(iso_name,isotope_dict):
    iso_list = determine_name(iso_name)
    peaks = ""
    prob = ""
    for x in range(len(iso_list)):
        for key,val in isotope_dict.items():
            if key[3:] == iso_list[x]:
                if x > 0:
                    peaks += "," + val['peaks']
                    prob += "," + val['probability']
                else:
                    peaks +=  val['peaks']
                    prob +=  val['probability']
    return [float(i) for i in peaks.split(',')],[float(i) for i in prob.split(',')]

def score_isotope(guess_name,true_name):
    score = 0
    if not true_name[0]=="":
        if len(guess_name) > len(true_name):
            return 1/len(guess_name)
        for i in range(len(true_name)):
            for j in range(len(guess_name)):
                if true_name[i] == guess_name[j]:
                    score += 1        
        return score/len(true_name)
    else:
        if len(guess_name) > 0:
            if len(guess_name) == 1 and guess_name[0] == 'ra-226':
                return 1
            else:
                return 0
        else:
            return 1

def xray_list(isotopes):
    xrays = np.array([])
    for key,val in isotopes.items():
        if val['xray']:
            for i in val['xray'].split(','):
                xrays = np.append(xrays,float(i))
    return xrays

def determine_isotope(all_peaks, all_prominences, isotopes):
    probabilities = np.zeros(len(isotopes))
    name = np.array([])
    index = 0
    for key, val in isotopes.items():
        probability = 1.0
        if val['xray']:
            xrays = np.array([])
            for i in val['xray'].split(','):
                xrays = np.append(xrays, float(i))
            peaks = np.array([])
            prominences = np.array([])
            for x in range(len(all_peaks)):
                if not any(abs(xray - all_peaks[x]) < 2 for xray in xrays):
                    peaks = np.append(peaks, all_peaks[x])
                    prominences = np.append(prominences, all_prominences[x])
                else:
                    probability *= 2
        else:
            peaks = all_peaks
            prominences = all_prominences
        name = np.append(name, key)
        iso_peaks = np.array([float(i) for i in val['peaks'].split(',')])
        prob_peaks = np.array([float(i) for i in val['probability'].split(',')])
        sorted_index_array = np.argsort(prob_peaks)
        sorted_iso_peaks = np.flip(iso_peaks[sorted_index_array], 0)
        sorted_prob_peaks = np.flip(prob_peaks[sorted_index_array], 0)
        sorted_ind_array = np.argsort(prominences)
        sorted_peaks = np.flip(peaks[sorted_ind_array], 0)
        sorted_prom_peaks = np.flip(prominences[sorted_ind_array], 0)
        for i in range(len(sorted_peaks)):
            for j in range(len(sorted_iso_peaks)):
                peak = sorted_peaks[i]
                iso_peak = sorted_iso_peaks[j]
                if abs(peak - iso_peak) < 2.5:
                    dist_factor = 1 - (abs(peak - iso_peak) / 2) * 0.1
                    iso_peak_prob = sorted_prob_peaks[j]
                    iso_peak_prob_frac = iso_peak_prob / max(prob_peaks)
                    prom_peak_frac = sorted_prom_peaks[i] / max(sorted_prom_peaks)
                    if abs(prom_peak_frac - iso_peak_prob_frac) < 0.25:
                        probability *= 10
                    elif abs(prom_peak_frac - iso_peak_prob_frac) < 0.35:
                        probability *= 8
                    elif abs(prom_peak_frac - iso_peak_prob_frac) < 0.38:
                        probability *= 5
                    elif abs(prom_peak_frac - iso_peak_prob_frac) < 0.46:
                        probability *= 2
                    if abs(i - j) < 3:
                        probability *= 10
                    if prom_peak_frac > 0.65:
                        probability *= 5
                    elif prom_peak_frac > 0.6:
                        probability *= 3
                    if iso_peak_prob_frac > 0.4 and iso_peak_prob_frac < 1:
                        probability *= 6
                    if peak < 90:
                        probability *= 0.1
                    elif peak < 100:
                        probability *= 0.6
        probabilities[index] = probability
        index += 1
    probabilities /= np.sum(probabilities)
    sorted_indices = np.argsort(probabilities)[::-1]
    top_5_indices = sorted_indices[:5]
    top_5_names = name[top_5_indices]
    top_5_probabilities = probabilities[top_5_indices]
    print("Top 5 Isotopes Identified:")
    for i in range(len(top_5_names)):
        print(f"{top_5_names[i][3:]}: {top_5_probabilities[i]:.4f}")
    return peaks, top_5_names, top_5_probabilities

# Modified plot_spectra to return the figure
def plot_spectra(file, counts, peaks, true_peaks=None, height_vec=None, x_lim=None, guess_nm=None, most_probable_isotope=None):
    rename_file = file.replace('.n42','')
    x = range(0,len(counts))
    fig = Figure(figsize=(5, 2.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.step(x, counts)
    if height_vec:
        ax.plot(x, height_vec, label="Threshold")
    ax.scatter([x[int(i)] for i in peaks], [counts[int(i)] for i in peaks], color='deepskyblue', label="Found peaks")
    ax.set_xlabel('Energy (keV)')
    ax.set_ylabel('Counts')
    ax.set_xlim(0, 1500)
    if x_lim:
        ax.set_xlim(right=x_lim)
    ax.set_title(f"Isotope ID: {most_probable_isotope}")
    return fig

# Modified isotopeID to return the figure and results
def isotopeID(file, counts, isotopes, compressed):
    spect = Spectra(file, counts, compressed)
    [peaks, peaks_dict] = find_peaks(spect.counts, prominence=spect.prom, width=spect.wdt_arr, rel_height=0.6, height=spect.height_vec, distance=4)
    final_peaks, guess_names, guess_probabilities = determine_isotope(peaks[peaks>42], peaks_dict['prominences'][peaks>42], isotopes)
    most_probable_index = np.argmax(guess_probabilities)
    most_probable_isotope = guess_names[most_probable_index]
    plt_peaks = peaks[peaks_dict['prominences']>0.1*np.mean(peaks_dict['prominences'])]
    fig = plot_spectra(file, spect.counts, plt_peaks, guess_nm=", ".join(guess_names), most_probable_isotope=most_probable_isotope)
    return fig, guess_names, guess_probabilities

# GUI Code
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Isotope Identification")
        self.root.geometry("800x600")

        # Apply a modern theme
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Create a frame for the top section
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.label = ttk.Label(self.top_frame, text="Select a .n42 file to process:", font=('Helvetica', 12))
        self.label.pack(side=tk.LEFT, padx=5, pady=5)

        self.file_path_label = ttk.Label(self.top_frame, text="No file selected", font=('Helvetica', 10))
        self.file_path_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.browse_button = ttk.Button(self.top_frame, text="Browse", command=self.browse_n42_file)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.txt_label = ttk.Label(self.top_frame, text="Select a .txt file for isotopes:", font=('Helvetica', 12))
        self.txt_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.txt_file_path_label = ttk.Label(self.top_frame, text="No file selected", font=('Helvetica', 10))
        self.txt_file_path_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.browse_txt_button = ttk.Button(self.top_frame, text="Browse", command=self.browse_txt_file)
        self.browse_txt_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.process_button = ttk.Button(self.top_frame, text="Process File", command=self.process_file)
        self.process_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a frame for the plot
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the results
        self.result_frame = ttk.Frame(root)
        self.result_frame.pack(fill=tk.X, padx=10, pady=10)

        self.result_label = ttk.Label(self.result_frame, text="Results will be displayed here", font=('Helvetica', 12))
        self.result_label.pack(pady=10)

        self.isotopes = {}

    def browse_n42_file(self):
        self.n42_file_path = filedialog.askopenfilename(filetypes=[("N42 files", "*.n42")])
        self.file_path_label.config(text=self.n42_file_path)

    def browse_txt_file(self):
        self.txt_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.txt_file_path_label.config(text=self.txt_file_path)

    def process_file(self):
        if hasattr(self, 'n42_file_path') and ".n42" in self.n42_file_path and os.path.exists(self.n42_file_path):
            if hasattr(self, 'txt_file_path') and ".txt" in self.txt_file_path and os.path.exists(self.txt_file_path):
                # Read in isotope database
                with open(self.txt_file_path) as f:
                    for lines in f.readlines():
                        line = lines.split(';')
                        xray = None
                        if len(line[3]) > 0:
                            xray = line[3].replace('\n','')
                        self.isotopes[line[0].lower()] = {'peaks':line[1],'probability':line[2].replace('\n',''),'xray':xray}
                f.close()

                with open(self.n42_file_path) as reader:
                    data = reader.readlines()
                    if data[1].count("xmlns") > 1:
                        data[1] = "<RadInstrumentData xmlns='http://physics.nist.gov/N42/2011/N42'>\n"
                with open(self.n42_file_path, 'w') as file:
                    file.writelines(data)
                RadInstrumentData = xmlwrapper.xmlread(self.n42_file_path)
                counts = RadInstrumentData.RadMeasurement.Spectrum[1].ChannelData.text
                compressed = True
                fig, guess_names, guess_probabilities = isotopeID(self.n42_file_path, counts, self.isotopes, compressed)

                # Display the plot in the GUI
                self.display_plot(fig)

                # Display the results
                result_text = "Top Isotopes Identified:\n"
                for i in range(len(guess_names)):
                    result_text += f"{guess_names[i][3:]}: {guess_probabilities[i]:.4f}\n"
                self.result_label.config(text=result_text)
            else:
                messagebox.showerror("Error", "Incorrect .txt file type or file not selected!")
        else:
            messagebox.showerror("Error", "Incorrect .n42 file type or file not selected!")

    def display_plot(self, fig):
        # Clear previous plot
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        # Embed the new plot
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Use a modern theme
    app = App(root)
    root.mainloop()