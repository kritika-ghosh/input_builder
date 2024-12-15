import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import os

# Atomic numbers mapping: A dictionary mapping element symbols to their atomic numbers
ATOMIC_NUMBERS = {
    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9,
    'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17,
    'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25,
    'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33,
    'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41,
    'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49,
    'Sn': 50, 'Sb': 51, 'I': 53, 'Te': 52, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57,
    'Ce': 58, 'Pr': 59, 'Nd': 60, 'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65,
    'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71, 'Hf': 72, 'Ta': 73,
    'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80, 'Tl': 81,
    'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89,
    'Th': 90, 'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97,
    'Cf': 98, 'Es': 99, 'Fm': 100, 'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104,
    'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109, 'Ds': 110, 'Rg': 111,
    'Cn': 112, 'Uut': 113, 'Fl': 114, 'Uup': 115, 'Lv': 116, 'Uus': 117, 'Uuo': 118
}

class GamessOptGUI:
    def __init__(self, root):
        # Set appearance mode and theme for the GUI
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize the main window
        self.root = root
        self.root.title("GAMESS Input File Builder")

        # Create a frame to contain the widgets
        frame = ctk.CTkFrame(root)
        frame.pack(padx=10, pady=10)

        # Dictionary to store input fields with their default values
        self.fields = {
            "Memory (MW)": tk.StringVar(value="50"),        # Default memory in MB
            "Memory DDI": tk.StringVar(value="30"),         # Default DDI memory
            "Spin": tk.StringVar(value="1"),                # Default spin state
            "Charge": tk.StringVar(value="0"),              # Default charge
            "Output File Name": tk.StringVar(value="optg.inp"),  # Default output file name
        }

        # Available options for method, runtype, basis set, and scftyp
        self.method_options = ["b3lyp", "mp2", "ump2", "ccsd", "uccsd"]
        self.method_var = tk.StringVar(value=self.method_options[0])

        self.runtype_options = ["OPTIMIZE", "ENERGY"]
        self.runtype_var = tk.StringVar(value=self.runtype_options[0])

        self.basis_set_options = ["AM1", "PM3", "PM6", "STO-3G", "3-21G", "6-31G*", "6-311G**", "6-311+G**", "aug-cc-pVDZ", "SPK-DZP"]
        self.basis_set_var = tk.StringVar(value=self.basis_set_options[0])

        self.scftyp_options = ["RHF", "UHF", "ROHF"]
        self.scftyp_var = tk.StringVar(value=self.scftyp_options[0])

        row = 0

        # Create input fields for the user to enter parameters
        for label, var in self.fields.items():
            ctk.CTkLabel(frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
            ctk.CTkEntry(frame, textvariable=var, width=70).grid(row=row, column=1, padx=5)
            row += 1

        # Dropdown for selecting the method (e.g., B3LYP, MP2)
        ctk.CTkLabel(frame, text="Method").grid(row=row, column=0, sticky="w", pady=5)
        self.method_dropdown = ctk.CTkOptionMenu(frame, variable=self.method_var, values=self.method_options)
        self.method_dropdown.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # Dropdown for selecting the RUNTYPE (e.g., OPTIMIZE, ENERGY)
        ctk.CTkLabel(frame, text="RUNTYPE").grid(row=row, column=0, sticky="w", pady=5)
        self.runtype_dropdown = ctk.CTkOptionMenu(frame, variable=self.runtype_var, values=self.runtype_options)
        self.runtype_dropdown.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # Dropdown for selecting SCFTYP (e.g., RHF, UHF)
        ctk.CTkLabel(frame, text="SCFTYP").grid(row=row, column=0, sticky="w", pady=5)
        self.scftyp_dropdown = ctk.CTkOptionMenu(frame, variable=self.scftyp_var, values=self.scftyp_options)
        self.scftyp_dropdown.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # Dropdown for selecting the basis set
        ctk.CTkLabel(frame, text="Basis set").grid(row=row, column=0, sticky="w", pady=5)
        self.basis_set_dropdown = ctk.CTkOptionMenu(frame, variable=self.basis_set_var, values=self.basis_set_options)
        self.basis_set_dropdown.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # Button to upload the geometry file
        ctk.CTkButton(frame, text="Upload Geometry File", command=self.upload_geometry_file).grid(
            row=row, column=0, columnspan=2, pady=10
        )

        # Button to generate the GAMESS input file
        ctk.CTkButton(frame, text="Generate Input File", command=self.generate_input_file).grid(
            row=row + 1, column=0, columnspan=2, pady=10
        )

        # Store geometry data
        self.geometry_data = ""

    def upload_geometry_file(self):
        """Allows the user to upload a geometry file and process its content."""
        # Open a file dialog to select an XYZ geometry file
        file_path = filedialog.askopenfilename(title="Select XMOL File", filetypes=[("XYZ files", "*.xyz")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    lines = file.readlines()[2:]  # Skip the first two lines which are metadata
                    geometry_lines = []

                    # Process the lines containing atomic coordinates
                    for line in lines:
                        parts = line.split()
                        if len(parts) >= 4:
                            element = parts[0]
                            x, y, z = parts[1:4]
                            atomic_number = ATOMIC_NUMBERS.get(element, 0)
                            geometry_lines.append(f"{element}  {atomic_number}\t{x}\t{y}\t{z}")

                    # Join the processed geometry data
                    self.geometry_data = "\n".join(geometry_lines)
                messagebox.showinfo("Success", "XMOL file loaded and processed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def generate_input_file(self):
        """Generates the GAMESS input file based on user inputs."""
        try:
            # Collect input values from the fields and dropdowns
            config = {key: var.get() for key, var in self.fields.items()}

            # Ensure geometry data is not empty
            if not self.geometry_data:
                raise ValueError("Geometry data cannot be empty! Please upload a geometry file.")

            method = self.method_var.get()
            runtype = self.runtype_var.get()
            scftyp = self.scftyp_var.get()
            basis_set = self.basis_set_var.get()

            # Set level of theory based on selected method
            if method.lower() in ["mp2", "ump2"]:
                level = "MPLEVL=2"
            elif method.lower() in ["ccsd", "uccsd"]:
                level = "CCTYP=CCSD"
            else:
                level = f"DFTTYP={method}"

            # Set basis set definition based on selected option
            if basis_set == "6-311G**":
                basis_definition = "GBASIS=N311 NGAUSS=6 NDFUNC=1 NPFUNC=1"
            else:
                basis_definition = f"GBASIS={basis_set}"

            # Create the GAMESS input file template
            template = f"""
$CONTRL SCFTYP={scftyp} {level} RUNTYP={runtype} ICHARG={config['Charge']}
COORD=UNIQUE MULT={config['Spin']} MAXIT=200 ISPHER=1 $END
$SYSTEM MWORDS={config['Memory (MW)']} MEMDDI={config['Memory DDI']} $END
$STATPT NSTEP=100 HSSEND=.T. $END
$BASIS {basis_definition} $END
$GUESS GUESS=HUCKEL $END
$DATA
optg and freq
C1
{self.geometry_data}
$END
""".strip()

            # Define the output file name
            output_file = os.path.join(os.getcwd(), config["Output File Name"])
            with open(output_file, "w") as f:
                f.write(template)

            messagebox.showinfo("Success", f"GAMESS input file '{output_file}' created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create input file: {e}")

# Main entry point for the application
if __name__ == "__main__":
    root = ctk.CTk()  # Create the main window
    app = GamessOptGUI(root)  # Create the GUI application instance
    root.mainloop()  # Run the main event loop to display the GUI
