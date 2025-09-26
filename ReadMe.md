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

---

### Getting Started for Developers

To run this application on your local machine, follow these steps.

**1. Clone the Repository**

First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/Hicham1970/DSApp.git
cd DSApp
```

**2. Install Dependencies**

This project's dependencies are listed in `requirements.txt`. It is highly recommended to use a virtual environment to keep your project dependencies isolated.

**a. Create and Activate a Virtual Environment**

From the project's root directory (`DSApp`), run the following commands:

```bash
# Create the virtual environment
python -m venv .venv
```

**3. Run the Application**

Once the dependencies are installed, you can run the application by executing the `main.py` script:

```bash
python main.py
```.


