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

        self.browse_button = ttk.Button(self.top_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

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
        self.isotopes_xray_path = "C:/Users/Jacob/Desktop/m400/isotopes_xray.txt"

        # Read in isotope database
        with open(self.isotopes_xray_path) as f:
            for lines in f.readlines():
                line = lines.split(';')
                xray = None
                if len(line[3]) > 0:
                    xray = line[3].replace('\n','')
                self.isotopes[line[0].lower()] = {'peaks':line[1],'probability':line[2].replace('\n',''),'xray':xray}
        f.close()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("N42 files", "*.n42")])
        self.file_path_label.config(text=self.file_path)

    def process_file(self):
        if hasattr(self, 'file_path') and ".n42" in self.file_path and os.path.exists(self.file_path):
            with open(self.file_path) as reader:
                data = reader.readlines()
                if data[1].count("xmlns") > 1:
                    data[1] = "<RadInstrumentData xmlns='http://physics.nist.gov/N42/2011/N42'>\n"
            with open(self.file_path, 'w') as file:
                file.writelines(data)
            RadInstrumentData = xmlwrapper.xmlread(self.file_path)
            counts = RadInstrumentData.RadMeasurement.Spectrum[1].ChannelData.text
            compressed = True
            fig, guess_names, guess_probabilities = isotopeID(self.file_path, counts, self.isotopes, compressed)

            # Display the plot in the GUI
            self.display_plot(fig)

            # Display the results
            result_text = "Top Isotopes Identified:\n"
            for i in range(len(guess_names)):
                result_text += f"{guess_names[i][3:]}: {guess_probabilities[i]:.4f}\n"
            self.result_label.config(text=result_text)
        else:
            messagebox.showerror("Error", "Incorrect file type or file not selected!")

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