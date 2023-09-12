import tkinter as tk
from tkinter import ttk
from p2 import InitialPage, FinalPage, BallastPage, RecapPage
from PIL import Image, ImageTk


class SettingsView(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # key : setting name (Language, Audio, ...)
        # value : Page object (ttk.Frame: Language page or Audio page)
        self.pages = {}

        # Give row 0 column 1 as room as it needs
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_frame_treeview().grid(row=0, column=0, stick='wns')
        self.create_frame_page().grid(row=0, column=2, sticky='ens')

    def create_frame_page(self) -> ttk.Frame:
        """
        Create the frame that will show the current setting page
        :return: ttk.Frame
        """
        self.frame_page = ttk.Frame(self)

        return self.frame_page

    def create_frame_treeview(self):
        """
        Create the frame on the left that will hold the setting treeview widget
         and instantiate the SettingTreeview Class and
          :returns: a ttk frame
          """
        self.frame_treeview = ttk.Frame(self, width=50)
        self.treeview_settings = SettingTreeview(self.frame_treeview)
        self.treeview_settings.bind(
            '<<TreeviewSelect>>', self.on_treeview_selection_changed)
        self.treeview_settings.pack(expand=True, fill='both')

        return self.frame_treeview

    def on_treeview_selection_changed(self, event):
        """
        # Switch to the frame related to the newly selected settings
        :param event:
        """
        selected_item = self.treeview_settings.focus()
        setting_name = self.treeview_settings.item(selected_item).get("text")

        self.show_page(setting_name)

    def show_page(self, setting_name: str):
        """
        pack.forget() all pages and pack the given page name
        :param setting_name: the setting/ page to show
        :return: None
        """
        for page_name in self.pages.keys():
            self.pages[page_name].pack_forget()
        # this code show the page according to the user selection
        self.pages[setting_name].pack(expand=False, fill='both')

    def add_page(self, image_path: str, setting_name: str, page):
        """
                Instantiate a page frame and add to the pages dictionary
                :param image_path: a path to an image file
                :param setting_name:(str)
                :param page: a page Class
                :return:None
                """

        # Load the image and convert it to a photo image
        with Image.open(image_path) as img:
            # convert it to a photo image
            photo_image = ImageTk.PhotoImage(img)

        # add page to dictionary so xe can show it when needed
        self.pages[setting_name] = page(self.frame_page)

        # Keep a reference to the image so that it doesn't get garbege collected
        self.pages[setting_name].image = photo_image

        # Insert the setting name into the settings treeview:
        self.treeview_settings.add_setting(
            image=photo_image, section_text=setting_name)


class SettingTreeview(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.heading("#0", text="Settings")

    def add_setting(self, image, section_text: str):
        """
        this method will insert a row to the treeview widget
        :param image: photo_image
        :param section_text: str
        :return:None
        """
        self.insert(parent="",
                    index=tk.END,
                    image=image,
                    text=section_text)
        self.pack(side='left')


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1347x1000')
    root.iconbitmap('ico.ico')
    root.title('Draft Survey App')
    root.state('zoomed')
    root.resizable(0, 0)
    # styling:
    style = ttk.Style()
    style.configure("Treeview.Heading",
                    relief="groove", background='gray34',
                    font=('times new roman', 15, 'bold')
                    )
    style.configure("Treeview",
                    rowheight=100,
                    font=('times new roman', 12, 'bold'),
                    background='orange')

    style.map("Treeview",
              foreground=[("selected", "dark green")],
              background=[("selected", "light green")])
    style.configure("TLabel", font=('times new roman', 16, 'bold'))

    ################################

    settings = SettingsView(root, relief='groove')

    settings.add_page(image_path='harbor-crane.png',
                      setting_name='Initial Draft',
                      page=InitialPage)
    settings.pack(fill='both', expand=True)

    settings.add_page(image_path='harbor-crane2.png',
                      setting_name='Final Draft',
                      page=FinalPage,
                      )
    settings.pack(fill='both', expand=True)

    settings.add_page(image_path='cargo-ship.png',
                      setting_name='Ballast',
                      page=BallastPage)
    settings.pack(fill='both', expand=True)

    settings.add_page(image_path='ship.png',
                      setting_name='Recap',
                      page=RecapPage)
    settings.pack(fill='both', expand=True)
    settings.add_page(image_path='ship.png',
                      setting_name='Recap',
                      page=RecapPage)
    settings.pack(fill='both', expand=True)

    root.mainloop()
