import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Import your library functions
from CompressibleFlowFunctions.Isentropic import *
from CompressibleFlowFunctions.Fanno import *
from CompressibleFlowFunctions.NSW import *
from CompressibleFlowFunctions.Expansion import *
from CompressibleFlowFunctions.misc import *

class FlowFunctionGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compressible Flow Functions GUI")
        self.geometry("650x450")
        self.create_widgets()

    def create_widgets(self):
        # Dropdown for module
        self.module_var = tk.StringVar()
        modules = ["Isentropic", "Fanno", "NSW", "Expansion", "Misc"]
        ttk.Label(self, text="Module:").pack(anchor="w")
        self.module_menu = ttk.Combobox(self, textvariable=self.module_var, values=modules, state="readonly")
        self.module_menu.pack(fill="x")
        self.module_menu.bind("<<ComboboxSelected>>", self.update_functions)

        # Dropdown for function
        self.func_var = tk.StringVar()
        ttk.Label(self, text="Function:").pack(anchor="w")
        self.func_menu = ttk.Combobox(self, textvariable=self.func_var, state="readonly")
        self.func_menu.pack(fill="x")
        self.func_menu.bind("<<ComboboxSelected>>", self.show_args)

        # Frame for arguments
        self.args_frame = ttk.LabelFrame(self, text="Arguments")
        self.args_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.arg_entries = {}

        # Run button
        self.run_btn = ttk.Button(self, text="Run", command=self.run_function)
        self.run_btn.pack(pady=5)

        # Output
        self.output_text = tk.Text(self, height=6)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

    def update_functions(self, event=None):
        module = self.module_var.get()
        func_dict = {
            "Isentropic": [
                "throat_area_from_mdot", "astar_all_else_known", "mach_from_G",
                "mach_from_aratio", "aratio_from_mach", "po_from_pratio",
                "p_from_pratio", "T_from_Tratio", "To_from_Tratio", "delta_mass_static"
            ],
            "Fanno": [
                "colebrook_white", "fanno_equation", "delta_fanno",
                "Lstar_fanno", "mach_fanno", "fanno_po_ratio"
            ],
            "NSW": [
                "prat_from_mach", "mach_from_pressure_ratio", "mach_after_shock",
                "pstatic_after_shock", "pstag_after_shock"
            ],
            "Expansion": [
                "prandtl_meyer", "mach_angle"
            ],
            "Misc": [
                "flowrates", "fanning_and_reynolds", "flowrates_choked",
                "flowrates_backwards", "mdot_to_scfh", "hole_numbers"
            ]
        }
        self.func_menu["values"] = func_dict.get(module, [])
        self.func_var.set("")
        self.clear_args()

    def show_args(self, event=None):
        self.clear_args()
        func_name = self.func_var.get()
        # Argument units dictionary
        arg_units = {
            "mdot": "kg/s",
            "Po": "Pa",
            "Rs": "J/kg·K",
            "To": "K",
            "gamma": "(dimensionless)",
            "Apipe": "m²",
            "M": "(dimensionless)",
            "Astar": "m²",
            "subsuper": "'subsonic' or 'supersonic'",
            "P": "Pa",
            "T": "K",
            "f": "(dimensionless)",
            "Re": "(dimensionless)",
            "D": "m",
            "epsilon": "μm",
            "L": "m",
            "Po1": "Pa",
            "Po2": "Pa",
            "M1": "(dimensionless)",
            "P2": "PSI",
            "P1": "PSI",
            "Cv": "(dimensionless)",
            "SG": "(dimensionless)",
            "Q": "SCFH",
            "Dpipe": "m",
            "mu": "Pa·s",
            "fluid": "name",
            "G": "(dimensionless)",
            "Dhole": "same as Astar",
            "A": "m²"
        }
        # Function descriptions
        func_descriptions = {
            "throat_area_from_mdot": "Calculates the minimum (choked) area required for a given mass flow and stagnation conditions.",
            "astar_all_else_known": "Calculates choking area and diameter from area ratio and Mach number.",
            "mach_from_G": "Finds Mach number from flow properties; resolves subsonic/supersonic branch.",
            "mach_from_aratio": "Finds Mach number from area ratio; resolves subsonic/supersonic branch.",
            "aratio_from_mach": "Calculates isentropic area ratio (A/A*) for a given Mach number.",
            "po_from_pratio": "Calculates stagnation pressure from static pressure and Mach number.",
            "p_from_pratio": "Calculates static pressure from stagnation pressure and Mach number.",
            "T_from_Tratio": "Calculates static temperature from stagnation temperature and Mach number.",
            "To_from_Tratio": "Calculates stagnation temperature from static temperature and Mach number.",
            "delta_mass_static": "Iterative equation for choked flow using mass flow and static pressure.",

            "colebrook_white": "Computes the Colebrook-White equation for Darcy friction factor.",
            "fanno_equation": "Calculates the Fanno equation value for a given Mach number and gamma.",
            "delta_fanno": "Returns the difference between both sides of the Fanno equation (for root finding).",
            "Lstar_fanno": "Directly calculates the Fanno choking length (L*) for given conditions.",
            "mach_fanno": "Calculates Mach number for a given pipe length using the Fanno equation.",
            "fanno_po_ratio": "Calculates the Fanno stagnation pressure ratio for a given Mach number and gamma.",

            "prat_from_mach": "Calculates the stagnation pressure ratio across a normal shock wave.",
            "mach_from_pressure_ratio": "Calculates the pre-shock Mach number for a desired stagnation pressure ratio.",
            "mach_after_shock": "Calculates the Mach number after a normal shock wave.",
            "pstatic_after_shock": "Calculates the static pressure after a normal shock wave.",
            "pstag_after_shock": "Calculates the stagnation pressure after a normal shock wave.",

            "prandtl_meyer": "Calculates the Prandtl-Meyer expansion angle (ν) for a given Mach number and gamma.",
            "mach_angle": "Calculates the Mach angle (μ) for a given Mach number.",

            "flowrates": "Calculates the static pressure drop through a flow device rated by Cv.",
            "fanning_and_reynolds": "Calculates Fanning friction factor and Reynolds number for a given flow.",
            "flowrates_choked": "Calculates the static pressure drop through a choked flow device rated by Cv.",
            "flowrates_backwards": "Iterates on inlet pressure for a given flow device and conditions.",
            "mdot_to_scfh": "Converts mass flow rate to standard cubic feet per hour (SCFH) for Nitrogen.",
            "hole_numbers": "Calculates the number of injector holes given choking area and drill diameter."
        }
        arg_lists = {
            "throat_area_from_mdot": ["mdot", "Po", "Rs", "To", "gamma"],
            "astar_all_else_known": ["Apipe", "M", "gamma"],
            "mach_from_G": ["Po", "Rs", "To", "gamma", "mdot", "Apipe", "subsuper"],
            "mach_from_aratio": ["Apipe", "Astar", "gamma", "subsuper"],
            "aratio_from_mach": ["M", "gamma"],
            "po_from_pratio": ["P", "gamma", "M"],
            "p_from_pratio": ["Po", "gamma", "M"],
            "T_from_Tratio": ["To", "gamma", "M"],
            "To_from_Tratio": ["T", "gamma", "M"],
            "delta_mass_static": ["M", "mdot", "P", "Rs", "To", "gamma", "A"],

            "colebrook_white": ["f", "Re", "D", "epsilon"],
            "fanno_equation": ["M", "gamma"],
            "delta_fanno": ["M", "L", "f", "D", "gamma"],
            "Lstar_fanno": ["f", "D", "M", "gamma"],
            "mach_fanno": ["L", "f", "D", "gamma"],
            "fanno_po_ratio": ["M", "gamma"],

            "prat_from_mach": ["gamma", "M"],
            "mach_from_pressure_ratio": ["Po1", "Po2", "gamma"],
            "mach_after_shock": ["M1", "gamma"],
            "pstatic_after_shock": ["M", "gamma", "P"],
            "pstag_after_shock": ["M", "gamma", "Po1"],

            "prandtl_meyer": ["M", "gamma"],
            "mach_angle": ["M"],

            "flowrates": ["P2", "P1", "Cv", "SG", "Q"],
            "fanning_and_reynolds": ["Po1", "To", "gamma", "M", "Rs", "Dpipe", "mu", "epsilon", "fluid"],
            "flowrates_choked": ["Cv", "SG", "Q"],
            "flowrates_backwards": ["P1", "P2", "Cv", "SG", "Q"],
            "mdot_to_scfh": ["mdot", "Rs", "G"],
            "hole_numbers": ["Dhole", "Astar"]
        }
        # Show function description at the top of the arguments frame
        desc = func_descriptions.get(func_name, "No description available.")
        desc_label = ttk.Label(self.args_frame, text=desc, wraplength=600, foreground="blue")
        desc_label.pack(anchor="w", pady=(0, 8))
        args = arg_lists.get(func_name, [])
        for arg in args:
            row = ttk.Frame(self.args_frame)
            row.pack(fill="x", pady=2)
            label_text = f"{arg} [{arg_units.get(arg, '')}]:" if arg in arg_units else f"{arg}:"
            ttk.Label(row, text=label_text).pack(side="left")
            entry = ttk.Entry(row)
            entry.pack(side="left", fill="x", expand=True)
            self.arg_entries[arg] = entry

    def clear_args(self):
        for widget in self.args_frame.winfo_children():
            widget.destroy()
        self.arg_entries = {}

    def run_function(self):
        module = self.module_var.get()
        func_name = self.func_var.get()
        args = []
        # Get argument values
        for arg, entry in self.arg_entries.items():
            val = entry.get()
            # Try to convert to float if possible, else keep as string
            try:
                val = float(val)
            except ValueError:
                pass
            args.append(val)
        # Map module to actual Python module
        module_map = {
            "Isentropic": globals(),
            "Fanno": globals(),
            "NSW": globals(),
            "Expansion": globals(),
            "Misc": globals()
        }
        # Try to call the function
        try:
            func = eval(func_name, module_map[module])
            result = func(*args)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Result: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Function call failed:\n{e}")

if __name__ == "__main__":
    app = FlowFunctionGUI()
    app.mainloop()