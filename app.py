import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys

from gui.mitre_gui import MitreView
from gui.malware_gui import MalwareBazaarView
from gui.api_gui import FortiEDRAPIView

# Always start in dark mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class FortiEDRDemoTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FortiEDR Demo Tool")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)
        self.iconbitmap(resource_path(os.path.join("assets", "fortinet.ico")))

        # Configure main grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Options + Results

        # Left Navigation Menu
        self.nav_frame = ctk.CTkFrame(self, width=120, fg_color="#2a2a2a")
        self.nav_frame.grid(row=0, column=0, sticky="ns")

        # Load logo
        logo_path = resource_path(os.path.join("assets", "fortinet-logo-white.png"))
        logo = Image.open(logo_path)
        w_percent = 130 / float(logo.size[0])
        h_size = int(float(logo.size[1]) * w_percent)
        logo_img = logo.resize((130, h_size), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(logo_img)
        self.logo_label = tk.Label(self.nav_frame, image=self.logo, bg="#2a2a2a")
        self.logo_label.grid(row=0, column=0, pady=(15, 5))

        def create_nav_button(parent, text, command):
            btn = ctk.CTkButton(parent, text=text, command=command, fg_color="#2e2e2e", hover_color="#444444", text_color="white", corner_radius=6, font=("Arial", 12, "bold"))
            return btn

        self.active_nav = None

        def set_active_nav(btn):
            if self.active_nav:
                self.active_nav.configure(fg_color="#2e2e2e", hover_color="#444444")
            btn.configure(fg_color="#FFA500", hover_color="#FFA500")
            self.active_nav = btn

        # Top buttons
        self.btn_mitre = create_nav_button(self.nav_frame, "MITRE", lambda: [self.show_mitre(), set_active_nav(self.btn_mitre)])
        self.btn_mitre.grid(row=1, column=0, pady=(10, 5), padx=10, sticky="ew")

        self.btn_malwarebazaar = create_nav_button(self.nav_frame, "Malware Bazaar", lambda: [self.show_malwarebazaar(), set_active_nav(self.btn_malwarebazaar)])
        self.btn_malwarebazaar.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        self.btn_api = create_nav_button(self.nav_frame, "FortiEDR API", lambda: [self.show_api(), set_active_nav(self.btn_api)])
        self.btn_api.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

        self.nav_frame.grid_rowconfigure(4, weight=1)

        # Bottom buttons
        self.fullscreen_btn = create_nav_button(self.nav_frame, "Full Screen", self.toggle_fullscreen)
        self.fullscreen_btn.grid(row=5, column=0, pady=5, padx=10, sticky="ew")
        self.fullscreen_btn.configure(fg_color="#4c566a", hover_color="#4c566a")

        self.quit_btn = create_nav_button(self.nav_frame, "Quit", self.quit)
        self.quit_btn.configure(fg_color="#cc0000", hover_color="#ff3333")
        self.quit_btn.grid(row=6, column=0, pady=(5, 20), padx=10, sticky="ew")

        # PanedWindow for Options and Results (grid inside column 1)
        self.paned_window = tk.PanedWindow(self, orient="horizontal", sashrelief="raised", sashwidth=8, bg="#1f1f1f")
        self.paned_window.grid(row=0, column=1, sticky="nsew")

        self.options_frame = ctk.CTkFrame(self.paned_window)
        self.results_frame = ctk.CTkFrame(self.paned_window)
        self.paned_window.add(self.options_frame, minsize=300)
        self.paned_window.add(self.results_frame)

        self.mitre_view = MitreView(self.options_frame, self.results_frame)
        self.malware_view = MalwareBazaarView(self.options_frame, self.results_frame)
        self.api_view = FortiEDRAPIView(self.options_frame, self.results_frame)

        self.show_mitre()
        set_active_nav(self.btn_mitre)

    def clear_frames(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def toggle_fullscreen(self):
        current_state = self.attributes("-fullscreen")
        self.attributes("-fullscreen", not current_state)
        if not current_state:
            self.fullscreen_btn.configure(fg_color="#4c566a", hover_color="#4c566a")
        else:
            self.fullscreen_btn.configure(fg_color="#1f1f1f", hover_color="#333333")


    def show_mitre(self):
        self.clear_frames()
        self.mitre_view = MitreView(self.options_frame, self.results_frame)

    def show_malwarebazaar(self):
        self.clear_frames()
        self.malware_view = MalwareBazaarView(self.options_frame, self.results_frame)

    def show_api(self):
        self.clear_frames()
        self.api_view = FortiEDRAPIView(self.options_frame, self.results_frame)

if __name__ == "__main__":
    app = FortiEDRDemoTool()
    app.mainloop()
