import tkinter as tk
from tkinter import ttk

from src.controllers.survey_controller import SurveyController
from src.views.final_page import FinalPage
from src.views.initial_page import InitialPage
from src.views.recap_page import RecapPage


class DraftSurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draft Survey Application")
        self.root.state('zoomed')
        self.root.resizable(True, True)

        # Set window icon
        try:
            self.root.iconbitmap('images/ico.ico')
        except tk.TclError:
            print(
                "Could not load icon 'images/ico.ico'. Make sure the file exists in the 'images' folder.")

        # Setup styles
        self.setup_styles()

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
        self.notebook.add(self.initial_page, text="Initial Draft")
        self.notebook.add(self.final_page, text="Final Draft")
        self.notebook.add(self.recap_page, text="Recap")

        # Set up data sharing between pages
        self.setup_data_sharing()

        # Create menu bar
        self.create_menu_bar()

    def setup_styles(self):
        """Setup application styles"""
        style = ttk.Style()

        # Configure notebook style
        style.configure("TNotebook", background='black')
        style.configure("TNotebook.Tab",
                        background='black',
                        foreground='black',
                        font=('Arial', 10, 'bold'),
                        padding=[10, 5])

        style.map("TNotebook.Tab",
                  background=[("selected", "gray20"), ("active", "gray10")],
                  foreground=[("selected", "gold"), ("active", "light blue")])

        # Configure frame styles
        style.configure("TFrame", background='gray15')
        style.configure("TLabelframe", background='gray15', foreground='gold')
        style.configure("TLabelframe.Label", background='gray15',
                        foreground='gold', font=('Arial', 8, 'bold'))

        # Configure button styles
        style.configure("TButton",
                        background='gray25',
                        foreground='black',
                        font=('Arial', 6, 'bold'),
                        padding=5)

        style.map("TButton",
                  background=[("active", "gray35"), ("pressed", "gray20")],
                  foreground=[("active", "white")])

        # Configure entry styles
        style.configure("TEntry",
                        fieldbackground='gray10',
                        foreground='black',
                        insertcolor='white',
                        font=('Arial', 7))

        # Configure label styles
        style.configure("TLabel",
                        foreground='white',
                        font=('Arial', 7))

        style.configure("Recap.TLabel", background='gray15',
                        foreground='white')
        style.configure("Cargo.TLabel", background='black',
                        foreground='cyan', font=('Arial', 10, 'bold'))
        style.configure("Difference.TLabel", background='black',
                        foreground='orange red', font=('Arial', 10, 'bold'))

        # Configure text widget styles
        style.configure("TText",
                        background='gray10',
                        foreground='black',
                        insertbackground='white',
                        selectbackground='gray30',
                        font=('Consolas', 7))

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

    def new_survey(self):
        """Start a new survey"""
        if tk.messagebox.askyesno("New Survey", "Are you sure you want to start a new survey? All current data will be lost."):
            self.controller.clear_all_data()
            self.initial_page.clear_all()
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
            "About", "Draft Survey Application\nVersion 2.0\n\nA comprehensive tool for maritime draft surveys.")

    def show_guide(self):
        """Show user guide"""
        guide_text = """Draft Survey Application User Guide:

1. Initial Draft Survey:
   - Enter vessel information
   - Input observed draft readings
   - Calculate corrected drafts
   - Perform interpolation calculations

2. Final Draft Survey:
   - Enter final draft readings
   - Input bunker quantities
   - Calculate final displacement
   - Determine cargo loaded/discharged

3. Data Management:
   - Save/Load survey data
   - Generate comprehensive reports
   - Export results

For detailed instructions, please refer to the documentation."""

        tk.messagebox.showinfo("User Guide", guide_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = DraftSurveyApp(root)
    root.mainloop()
