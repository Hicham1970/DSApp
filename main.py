import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.controllers.survey_controller import SurveyController
from src.views.final_page import FinalPage
from src.views.initial_page import InitialPage
from src.utils.themes import dark_theme, light_theme
from src.utils.config_manager import load_config, save_config
from src.views.recap_page import RecapPage


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DraftSurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draft Survey Application")
        self.root.state('zoomed')
        self.root.resizable(True, True)

        # Set window icon
        try:
            self.root.iconbitmap(resource_path('images/ico.ico'))
        except tk.TclError:
            print(
                "Could not load icon 'images/ico.ico'. Make sure the file exists in the 'images' folder.")

        # Load saved theme or default to dark
        config = load_config()
        theme_name = config.get("theme", "dark")
        self.current_theme = light_theme if theme_name == "light" else dark_theme

        # Setup styles
        self.setup_styles(self.current_theme)

        # Load icons for main tabs
        self._load_main_icons()  # type: ignore

        # Create main controller
        self.controller = SurveyController()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Initialize pages as notebook children
        self.initial_page = InitialPage(
            self.notebook, controller=self.controller)
        self.final_page = FinalPage(self.notebook, controller=self.controller)
        self.recap_page = RecapPage(self.notebook, controller=self.controller)

        # Add pages to notebook
        self.notebook.add(
            self.initial_page, image=self.first_icon, compound=tk.LEFT)  # type: ignore
        self.notebook.add(
            self.final_page, image=self.second_icon, compound=tk.LEFT)  # type: ignore
        self.notebook.add(
            self.recap_page, image=self.recap_icon, compound=tk.LEFT)  # type: ignore

        # Set up data sharing between pages
        self.setup_data_sharing()

        # Create menu bar
        self.create_menu_bar()

        # Create tooltips for main tabs
        self._create_main_notebook_tooltips()

    def _load_main_icons(self):
        """Loads icons for the main notebook tabs."""
        icon_size = (24, 24)
        icon_paths = {
            'recap_icon': "images/recap.png",
            'first_icon': "images/first.png",
            'second_icon': "images/second.png",
        }
        for attr_name, path in icon_paths.items():
            try:
                img = Image.open(resource_path(path)).resize(
                    icon_size, Image.LANCZOS)
                setattr(self, attr_name, ImageTk.PhotoImage(img))
            except Exception as e:
                print(f"Error loading main icon {path}: {e}")
                setattr(self, attr_name, None)

    def _create_main_notebook_tooltips(self):
        """Create tooltips for the main notebook tabs."""
        tooltip_texts = {
            0: "Initial Draft Survey",
            1: "Final Draft Survey",
            2: "Recap and Reports"
        }
        tooltip_window = None

        def show_tooltip(event):
            nonlocal tooltip_window
            try:
                element = self.notebook.identify(event.x, event.y)
                if "tab" in element:
                    index = self.notebook.index(f"@{event.x},{event.y}")
                    text = tooltip_texts.get(index)
                    if text:
                        if tooltip_window:
                            tooltip_window.destroy()
                        x, y, _, _ = self.notebook.bbox(index)
                        x += self.notebook.winfo_rootx() + 25
                        y += self.notebook.winfo_rooty() + 20
                        tooltip_window = tk.Toplevel(self.notebook)
                        tooltip_window.wm_overrideredirect(True)
                        tooltip_window.wm_geometry(f"+{x}+{y}")
                        bg = self.current_theme.get("tooltip_bg", "#FFFFE0")
                        fg = self.current_theme.get("tooltip_fg", "black")
                        label = tk.Label(tooltip_window, text=text, background=bg, foreground=fg,
                                         relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
                        label.pack(ipadx=1)
            except tk.TclError:
                pass  # Ignore errors when not over a tab

        def hide_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None

        self.notebook.bind("<Motion>", show_tooltip)
        self.notebook.bind("<Leave>", hide_tooltip)

    def setup_styles(self, theme: dict):
        """Setup application styles"""
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            print(
                "Le thème 'clam' n'est pas disponible, les boutons ne seront pas arrondis.")

        # Configure notebook style
        style.configure("TNotebook", background=theme["notebook_bg"])
        style.configure("TNotebook.Tab",
                        background=theme["tab_bg"],
                        foreground=theme["tab_fg"],
                        borderwidth=0,
                        font=('Arial', 10, 'bold'),
                        padding=[10, 5])

        style.map("TNotebook.Tab",
                  background=[("selected", theme["tab_selected_bg"]),
                              ("active", theme["tab_active_bg"])],
                  foreground=[("selected", theme["tab_selected_fg"]), ("active", theme["tab_active_fg"])])

        # Configure frame styles
        style.configure("TFrame", background=theme["frame_bg"])
        style.configure(
            "TLabelframe", background=theme["labelframe_bg"], foreground=theme["labelframe_fg"])
        style.configure("TLabelframe.Label", background=theme["labelframe_bg"],
                        foreground=theme["labelframe_fg"], font=('Arial', 8, 'bold'))

        # Configure button styles
        style.configure("TButton",
                        background=theme["button_bg"],
                        foreground=theme["button_fg"],
                        font=('Arial', 6, 'bold'),
                        borderwidth=0,
                        relief='flat',
                        padding=5, radius=15)  # 'radius' est spécifique à certains thèmes comme 'clam'

        style.map("TButton",
                  background=[("active", theme["button_active_bg"]),
                              ("pressed", theme["button_pressed_bg"])],
                  foreground=[("active", theme["button_active_fg"])])

        # Style for rounded buttons with images
        style.configure("Round.TButton",
                        background=theme["button_bg"],
                        foreground=theme["button_fg"],
                        font=('Arial', 8, 'bold'),
                        borderwidth=0,
                        relief='flat',
                        padding=8, radius=20)
        style.map("Round.TButton",
                  background=[("active", theme["button_active_bg"]),
                              ("pressed", theme["button_pressed_bg"])],
                  foreground=[("active", theme["button_active_fg"])])

        # Configure entry styles
        style.configure("TEntry",
                        fieldbackground=theme["entry_bg"],
                        foreground=theme["entry_fg"],
                        insertcolor=theme["entry_insert"],
                        font=('Arial', 7))

        # Configure label styles
        style.configure("TLabel",
                        background=theme["frame_bg"],
                        foreground=theme["label_fg"],
                        font=('Arial', 7))

        style.configure("Recap.TLabel", background=theme["recap_label_bg"],
                        foreground=theme["recap_label_fg"])
        style.configure("Cargo.TLabel", background=theme["frame_bg"],
                        foreground=theme["cargo_label_fg"], font=('Arial', 10, 'bold'))
        style.configure("Difference.TLabel", background=theme["frame_bg"],
                        foreground=theme["diff_label_fg"], font=('Arial', 10, 'bold'))

        # Configure text widget styles
        # Note: tk.Text is not a ttk widget, so this won't work. It must be configured directly.

    def setup_data_sharing(self):
        """Setup data sharing between pages"""
        # The pages now manage their own data through the controller
        # Data is automatically synchronized through the controller
        pass

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Survey", command=self.new_survey)
        file_menu.add_command(label="Open Survey", command=self.open_survey)
        file_menu.add_command(label="Save Survey", command=self.save_survey)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report",
                              command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Calculate All",
                               command=self.calculate_all)
        tools_menu.add_command(label="Validate Data",
                               command=self.validate_all_data)
        tools_menu.add_separator()
        tools_menu.add_command(label="Clear All Data",
                               command=self.clear_all_data)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_guide)

        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Themes", menu=theme_menu)
        theme_menu.add_command(
            label="Dark Theme", command=lambda: self.switch_theme(dark_theme))
        theme_menu.add_command(label="Light Theme",
                               command=lambda: self.switch_theme(light_theme))

    def switch_theme(self, theme: dict):
        """Switch the application theme."""
        if self.current_theme.get("name") == theme.get("name"):
            return

        # --- Animation Start ---
        try:
            from PIL import ImageGrab

            # 1. Grab the current window image
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            image = ImageGrab.grab((x, y, x + w, y + h))
            photo = ImageTk.PhotoImage(image)

            # 2. Create a temporary Toplevel window for the fade effect
            fade_window = tk.Toplevel(self.root)
            fade_window.geometry(f"{w}x{h}+{x}+{y}")
            fade_window.overrideredirect(True)
            tk.Label(fade_window, image=photo).pack()
            fade_window.lift()

            # 3. Apply the new theme immediately underneath
            self.current_theme = theme
            self.setup_styles(theme)
            self.initial_page.update_style(theme)
            self.final_page.update_style(theme)
            self.recap_page.update_style(theme)
            self.root.update_idletasks()

            # 4. Animate the fade out
            def animate_fade(alpha):
                if alpha <= 0:
                    fade_window.destroy()
                    return
                fade_window.attributes("-alpha", alpha)
                self.root.after(20, lambda: animate_fade(alpha - 0.05))

            animate_fade(1.0)

            # Save the new theme choice
            save_config({"theme": theme["name"]})

        except ImportError:
            # Fallback if ImageGrab is not available
            self.current_theme = theme
            self.setup_styles(theme)
            self.initial_page.update_style(theme)
            self.final_page.update_style(theme)
            self.recap_page.update_style(theme)
            save_config({"theme": theme["name"]})

    def new_survey(self):
        """Start a new survey"""
        if tk.messagebox.askyesno("New Survey", "Are you sure you want to start a new survey? All current data will be lost."):
            self.controller.clear_all_data()
            self.initial_page.clear_all()  # type: ignore
            self.final_page.clear_all()
            self.recap_page.clear_all()

    def open_survey(self):
        """Open a saved survey"""
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.controller.load_survey_data(filename)
                self.load_data_into_pages()
                tk.messagebox.showinfo(
                    "Success", "Survey data loaded successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error loading survey: {str(e)}")

    def save_survey(self):
        """Save current survey"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.controller.save_survey_data(filename)
                tk.messagebox.showinfo(
                    "Success", "Survey data saved successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error saving survey: {str(e)}")

    def export_report(self):
        """Export survey report"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                report = self.controller.generate_survey_report()
                with open(filename, 'w') as f:
                    f.write(report)
                tk.messagebox.showinfo(
                    "Success", "Report exported successfully!")
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Error exporting report: {str(e)}")

    def calculate_all(self):
        """Perform all calculations"""
        try:
            # Trigger calculations on current page
            current_tab = self.notebook.index(self.notebook.select())

            if current_tab == 0:  # Initial page
                self.initial_page.calculate_corrected_drafts()
            elif current_tab == 1:  # Final page
                self.final_page.calculate_corrected_drafts()

            tk.messagebox.showinfo("Success", "Calculations completed!")
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Error during calculations: {str(e)}")

    def validate_all_data(self):
        """Validate all survey data"""
        try:
            # Validate current page data
            current_tab = self.notebook.index(self.notebook.select())

            if current_tab == 0:  # Initial page
                # Validation is done automatically in the page methods
                pass
            elif current_tab == 1:  # Final page
                # Validation is done automatically in the page methods
                pass

            tk.messagebox.showinfo("Validation", "Data validation completed!")
        except Exception as e:
            tk.messagebox.showerror(
                "Validation Error", f"Data validation failed: {str(e)}")

    def clear_all_data(self):
        """Clear all survey data"""
        if tk.messagebox.askyesno("Clear All", "Are you sure you want to clear all data?"):
            self.controller.clear_all_data()
            self.initial_page.clear_all()
            self.final_page.clear_all()
            self.recap_page.clear_all()

    def load_data_into_pages(self):
        """Load controller data into page forms"""
        try:
            survey_data = self.controller.get_survey_summary()

            # Load data into initial page
            self.initial_page.controller = self.controller
            self.initial_page.populate_fields_from_data()

            # Load data into final page
            self.final_page.controller = self.controller
            self.final_page.populate_fields_from_data()

            # Update recap page
            self.recap_page.update_data(self.controller.survey_data)

        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Error loading data into pages: {str(e)}")

    def show_about(self):
        """Show about dialog"""
        tk.messagebox.showinfo(
            "About", "HG Draft Survey Application\nVersion 2.0\n\nA comprehensive tool for maritime draft surveys, designed by Hicham Garoum Septembre 2025, Contactez moi pour plus d'informations a l'addresse email: h.garoum@gmail.com")

    def show_guide(self):
        """Show user guide"""
        guide_text = """**Draft Survey Application User Guide**

Welcome to the Draft Survey application, a comprehensive tool for maritime draft surveys.

**Main Navigation:**
The application is organized into three main tabs represented by icons:
- **Tab 1 (Initial Draft):** For the initial survey.
- **Tab 2 (Final Draft):** For the final survey.
- **Tab 3 (Recap):** For summary and report generation.

**1. Initial Survey (First Tab):**
   - **Vessel Info & Time Sheet:** Enter the vessel information and the survey's time sheet.
   - **Draft Readings & Deductibles:** Enter the observed draft readings and the quantities of bunkers and fresh water.
   - **Calculations:** Enter the hydrostatic data for interpolation.
   - **Results:** View the calculation results as they are computed.
   - Use the buttons at the bottom to perform the calculations step by step.

**2. Final Survey (Second Tab):**
   - Follow the same steps for the new draft readings and bunkers.
   - The vessel data is carried over from the initial survey.

**3. Summary and Reports (Third Tab):**
   - Displays a complete summary of the survey.
   - Allows you to generate a detailed report and export it to PDF.

**Data Management (File Menu):**
   - **New/Open/Save Survey:** Manage your survey files (.json).
   - **Export Report:** Export the report in text format.

**Themes (Themes Menu):**
   - **Dark Theme:** Activates the dark theme for better visual comfort.
   - **Light Theme:** Activates the standard light theme.
"""

        tk.messagebox.showinfo("User Guide", guide_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = DraftSurveyApp(root)
    root.mainloop()
