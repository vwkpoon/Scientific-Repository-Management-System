# HKUST
#SID: 20882882
# for isbn test here is the sample number 9780618260300
import os
import csv
import tkinter as tk
from tkinter import ttk,scrolledtext,font,filedialog
import tkinter.messagebox as messagebox
import subprocess
from datetime import datetime
import webbrowser
import re

class Material:
    def __init__(self, typeofmaterial, title, authors, year, abstract,subject,
                month=None, day=None,
                 keywords_1=None, keywords_2=None, keywords_3=None,
                 keywords_4=None, url=None, doi=None,
                 publisher=None, edition=None, isbn=None, note=None,
                 file_path=None, tag=None):
        self.type = typeofmaterial
        self.title = title
        self.authors = self.get_unique_authors(authors)
        self.year = year
        self.abstract = abstract
        self.subject = subject
        self.month = month
        self.day = day
        self.keywords1 = keywords_1
        self.keywords2 = keywords_2
        self.keywords3 = keywords_3
        self.keywords4 = keywords_4
        self.url = url
        self.doi = doi
        self.publisher = publisher
        self.edition = edition
        self.isbn = isbn
        self.note = note
        self.file_path = file_path
        self.tag = tag
    def get_unique_authors(self, authors):
        if authors:
            author_list = [author.strip() for author in authors.split(',')]
            return set(author_list)
        return set()

class MaterialManager:
    def __init__(self, filename):
        self.filename = filename
        self.materials = self.read_or_create_csv()

# csv
    def read_or_create_csv(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                materials = [
                    Material(
                        row[0], row[1], row[2], row[3], row[4], row[5],
                        row[6] if row[6] else 0,
                        row[7] if row[7] else 0,
                        row[8], row[9], row[10], row[11], row[12], row[13],
                        row[14], row[15], row[16], row[17], row[18],row[19]
                    )
                    for row in reader
                ]
        else:
            materials = []
        return materials

    def save_to_csv(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'Title', 'Authors', 'Year',  'Abstract','Subject', 'Month', 'Day','Keywords 1',
                             'Keywords 2', 'Keywords 3', 'Keywords 4', 'URL', 'DOI', 'Publisher', 'Edition',
                             'ISBN', 'Note', 'File Path','Tag'])  # Write the header row
            for material in self.materials:
                authors_str = ', '.join(material.authors)
                writer.writerow([material.type, material.title, authors_str, material.year, material.abstract, material.subject, 
                                 material.month,material.day, material.keywords1,
                                 material.keywords2, material.keywords3, material.keywords4, material.url,
                                 material.doi, material.publisher, material.edition, material.isbn, material.note,
                                 material.file_path,material.tag])

#-----SEARCH FUNCTION-----#
# simple search code
    def search_material(self):
        search_option = self.search_option_var.get()
        keyword = self.search_entry_var.get()

        if search_option == "Title":
            results = [material for material in self.materials if keyword.lower() in material.title.lower()]
        elif search_option == "Authors":
            results = [material for material in self.materials if any(keyword.lower() in author.lower() for author in material.authors)]
        elif search_option == "Keywords":
            results = [material for material in self.materials if any(keyword.lower() in keyword_attr.lower() for keyword_attr in 
                                                                    [material.keywords1, material.keywords2, material.keywords3, material.keywords4])]
        elif search_option == "Subject":
            results = [material for material in self.materials if keyword.lower() in material.subject.lower()]

        self.display_search_results(results)

# simple sort result
    def sort_results(self, results):
        sort_option = self.sort_option_var.get()

        if sort_option == "Title":
            sorted_results = sorted(results, key=lambda material: material.title)
        elif sort_option == "Date_Older":
            sorted_results = sorted(results, key=lambda material: (int(material.year), int(material.month), int(material.day)))
        elif sort_option == "Date_Newest":
            sorted_results = sorted(results, key=lambda material: (int(material.year), int(material.month), int(material.day)), reverse=True)

        self.result_window.destroy()  # Close the previous result window
        self.display_search_results(sorted_results)  # Open a new result window with the sorted results    
# display search    
    def display_search_results(self, results):
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("Search Results")
        self.result_window.geometry("600x500")

        if results:
            self.result_listbox = tk.Listbox(self.result_window, width=80, height=20)
            scrollbar = tk.Scrollbar(self.result_window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.result_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.result_listbox.yview)
            
            x_scrollbar = tk.Scrollbar(self.result_window, orient=tk.HORIZONTAL)
            x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            self.result_listbox.config(xscrollcommand=x_scrollbar.set)
            x_scrollbar.config(command=self.result_listbox.xview)

            for material in results:
                self.result_listbox.insert(tk.END, f"Type:{material.type} Title: {material.title}  Authors: {material.authors}  Year: {material.year} Subject: {material.subject}")
                self.result_listbox.bind('<<ListboxSelect>>', lambda event: self.display_material_details(event, results))
                self.result_listbox.pack()
        else:
            entry_word = self.search_entry_var.get()
            result_label = ttk.Label(self.result_window, text=f"There are no results matching your search: {entry_word}")
            result_label.pack()

            result_label.configure(font=font.Font(weight='bold'))

            suggestions_label = tk.Label(self.result_window, text="Suggestions:")
            suggestions_label.pack()

            suggestions = [
                "Make sure that all words are spelled correctly.",
                "Try a different search scope.",
                "Try different search terms.",
                "Try more general search terms.",
                "Try fewer search terms."
            ]

            for suggestion in suggestions:
                suggestion_label = tk.Label(self.result_window, text=suggestion)
                suggestion_label.pack()

        sort_button = tk.Button(self.result_window, text="Sort Results", command=lambda: self.sort_results(results))
        sort_button.pack()
        
        self.sort_option_var = tk.StringVar()
        sort_option_menu = ttk.OptionMenu(self.result_window, self.sort_option_var, "Title", "Title", "Date_Older","Date_Newest")
        sort_option_menu.pack()
               
# select material    
    def display_material_details(self, event, results):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            material = results[index]
            self.display_material_toplevel(material)


    def display_material_toplevel(self, material):
        info_window = tk.Toplevel()
        info_window.title("Material Details")
        info_window.geometry("550x300")

        # create a frame for the buttons
        button_frame = tk.Frame(info_window)
        button_frame.grid(row=0, column=1, sticky='n')

        # create a frame for the labels
        label_frame = tk.Frame(info_window, width=800, height=800)
        label_frame.grid(row=0, column=0)
        label_frame.grid_propagate(False)

        # create a ScrolledText widget for the labels
        st = scrolledtext.ScrolledText(label_frame, width=60, height=20)
        st.pack()

        delete_button = tk.Button(button_frame, text="Delete", command=lambda: self.delete_material(material, info_window))
        delete_button.pack(side=tk.TOP)

        edit_button = tk.Button(button_frame, text="Edit", command=lambda: self.edit_material(material))
        edit_button.pack(side=tk.TOP)
        
        openurl_button = tk.Button(button_frame, text="Open Link", command=lambda: self.open_selected_url(material))
        openurl_button.pack(side=tk.TOP)

        openfile_button = tk.Button(button_frame, text="Open File", command=lambda: self.open_selected_file(material))
        openfile_button.pack(side=tk.TOP)

        tag_button = tk.Button(button_frame, text="Tag", command=lambda: self.add_tag(material))
        tag_button.pack(side=tk.TOP)

        # use the insert method of the ScrolledText widget to add the labels
        st.insert(tk.END, f"Type of Material: {material.type}\n")
        st.insert(tk.END, f"Title: {material.title}\n")
        st.insert(tk.END, f"Author(s): {material.authors}\n")
        st.insert(tk.END, f"Date: {material.day}/{material.month}/{material.year}\n")
        st.insert(tk.END, f"Subject: {material.subject}\n")
        st.insert(tk.END, f"Keyword(s): {material.keywords1}/{material.keywords2}/{material.keywords3}/{material.keywords4}\n")
        if material.doi:
            st.insert(tk.END, f"DOI: {material.doi}\n")
        if material.publisher:
            st.insert(tk.END, f"publisher: {material.publisher}\n")
        if material.edition:
            st.insert(tk.END, f"Edition: {material.edition}\n")
        if material.isbn:
            st.insert(tk.END, f"ISBN: {material.isbn}\n")
        st.insert(tk.END, f"Abstract: {material.abstract}\n")
        st.insert(tk.END, f"Note: {material.note}\n")
        st.insert(tk.END, f"URL/Link: {material.url}\n")
        st.insert(tk.END, f"File_path: {material.file_path}\n")

        # disable the widget so the user can't edit the text
        st.config(state=tk.DISABLED)

# advanced search function
    def advanced_search_material(self, type=None, year_range=None, title=None, keywords=None, subject=None):
        results = self.materials

        if type is not None and type != "Any":
            results = [material for material in results if material.type == type]

        if year_range is not None:
            start_year, end_year = year_range
            results = [material for material in results if int(start_year) <= int(material.year) <= int(end_year)]

        if title is not None:
            results = [material for material in results if title.lower() in material.title.lower()]

        if keywords is not None:
            results = [material for material in results if any(keywords.lower() in material_attr.lower() for material_attr in 
                                                            [material.keywords1, material.keywords2, material.keywords3, material.keywords4])]
        if subject is not None:
            results = [material for material in results if subject.lower() in material.subject.lower()]
        
        self.display_search_results(results)
        
    def open_advanced_search_window(self):
        self.advanced_search_window = tk.Toplevel(self.root)
        self.advanced_search_window.title("Advanced Search")
        self.advanced_search_window.geometry("400x300")

        # Type OptionMenu
        self.type_var = tk.StringVar(self.advanced_search_window)
        self.type_var.set("Any")  # default value
        type_option_menu = tk.OptionMenu(self.advanced_search_window, self.type_var, 
                                        "Any", "Database", "Research Paper", "Book", "Article", "Conference Paper","Other")
        type_option_menu.pack()

        # Year Range Entry
        year_range_label = tk.Label(self.advanced_search_window, text="Year Range (start-end):")
        year_range_label.pack()
        self.year_range_entry_var = tk.StringVar()
        year_range_entry = tk.Entry(self.advanced_search_window, textvariable=self.year_range_entry_var)
        year_range_entry.pack()

        # Title Entry
        title_label = tk.Label(self.advanced_search_window, text="Title:")
        title_label.pack()
        self.title_entry_var = tk.StringVar()
        title_entry = tk.Entry(self.advanced_search_window, textvariable=self.title_entry_var)
        title_entry.pack()

        # Keywords Entry
        keywords_label = tk.Label(self.advanced_search_window, text="Keywords:")
        keywords_label.pack()
        self.keywords_entry_var = tk.StringVar()
        keywords_entry = tk.Entry(self.advanced_search_window, textvariable=self.keywords_entry_var)
        keywords_entry.pack()

        # Subject Entry
        subject_label = tk.Label(self.advanced_search_window, text="Subject:")
        subject_label.pack()
        self.subject_entry_var = tk.StringVar()
        subject_entry = tk.Entry(self.advanced_search_window, textvariable=self.subject_entry_var)
        subject_entry.pack()

        # Advanced Search Button
        search_button = tk.Button(self.advanced_search_window, text="Search", command=self.call_advanced_search_material)
        search_button.pack()

    def call_advanced_search_material(self):
        type = self.type_var.get()
#mistake
        #year_range = tuple(map(int, self.year_range_entry_var.get().split('-')))
#updated       
        year_range_entry_value = self.year_range_entry_var.get()
        year_range = None

        if year_range_entry_value:
            start_year, end_year = map(int, year_range_entry_value.split('-'))
            year_range = (start_year, end_year)
            
        title = self.title_entry_var.get()
        keywords = self.keywords_entry_var.get()
        subject = self.subject_entry_var.get()
        self.advanced_search_material(type=type, year_range=year_range, title=title, keywords=keywords, subject=subject)

#---------------search function---------------------#

#----edit----#
    def edit_material(self, material):
        EditForm(material, self)

# delete function    
    def save_to_recycle_bin_csv(self, material):
        recycle_bin_filename = "20882882recycle_bin.csv"
        with open(recycle_bin_filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            authors_str = ', '.join(material.authors)
            writer.writerow([material.type, material.title, authors_str, material.year, material.abstract, material.subject, 
                                 material.month,material.day, material.keywords1,
                                 material.keywords2, material.keywords3, material.keywords4, material.url,
                                 material.doi, material.publisher, material.edition, material.isbn, material.note,
                                 material.file_path,material.tag])
    
    def delete_material(self,material,toplevel):
        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this Material?")
        if confirmation:
            self.materials.remove(material)
            self.save_to_csv()
            self.save_to_recycle_bin_csv(material)
            messagebox.showinfo("Deletion Successful", "The material has been deleted and moved to the recycle bin.")
            toplevel.destroy()  # Destroy the top-level window
            self.update_recent_materials()
        else:
            messagebox.showinfo("Deletion Cancelled", "The material deletion has been cancelled.")
                 
    def open_recycle_bin_window(self):
        recycle_window = tk.Toplevel()
        recycle_window.title("Recycle Bin")
        
        recycle_bin = RecycleBin(recycle_window, self)  # Pass the instance of the MaterialManager to RecycleBin
        recycle_bin.show_recycle_bin_window()
         
    def restore_material(self,material_data):
        type, title, authors_str, year, abstract, subject, month,day, keywords1,keywords2, keywords3, keywords4, url,doi,publisher, edition, isbn, note,file_path,tag = material_data
        material = Material(type, title, authors_str, year, abstract, subject, month,day, keywords1,keywords2, keywords3, keywords4, url,doi,publisher, edition, isbn, note, file_path,tag)
        self.materials.append(material)
        # Save the updated material data to the CSV file
        self.save_to_csv() 
        self.update_recent_materials()
#-------------------------  delete & restore function done ---------------------#
#open URL
    def open_selected_url(self, material):
        url = material.url
        if url:
            webbrowser.open_new_tab(url)
        else:
            messagebox.showerror("Error", "No URL/Link available.")
#open file (base the location)
    def open_selected_file(self, material):
        
        file_path = material.file_path

        # Check if the file path is not None and the file exists
        if file_path and os.path.isfile(file_path):
            # Open the file
            if os.name == 'nt':  # If the OS is Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # If the OS is Unix or Linux
                subprocess.call(('xdg-open', file_path))
        else:
            # Show an error if the file doesn't exist
            messagebox.showerror("Error", "File does not exist.")
     
# link with class addmaterialform    
    def add_material(self):
        add_window = tk.Toplevel()
        add_window.title("Add Material")

        AddMaterialFrom(add_window, self.materials, self.save_to_csv, self.update_recent_materials)
# recent materials
    def update_recent_materials(self):
        # Clear the recent materials listbox
        self.recent_listbox.delete(0, tk.END)

        # Read the CSV file and get the recent materials
        self.recent_materials = self.materials[-10:]  # Get the last 10 materials (you can change the number as needed)

        # Display the recent materials in the listbox
        for material in self.recent_materials:
            self.recent_listbox.insert(tk.END, f"Type:{material.type} Title: {material.title}  Authors: {material.authors}  Year: {material.year} Subject: {material.subject}")

        self.recent_listbox.bind("<<ListboxSelect>>", self.display_recentmaterial_details)
    def display_recentmaterial_details(self, event):
        selected_indices = self.recent_listbox.curselection()
        if selected_indices:
            index = int(selected_indices[0])
            material = self.recent_materials[index]
            self.display_material_toplevel(material)

#tag
    def add_tag(self, material):
        tag_name = tk.simpledialog.askstring("Add Tag", "Enter a tag name:", initialvalue=material.tag)
        if tag_name is not None:
            material.tag = tag_name
            self.save_to_csv()
            messagebox.showinfo("Tag Added", "Tag has been added successfully.")
    def show_tag(self):
        tags = set()
        for material in self.materials:
            if material.tag:
                tags.add(material.tag)

        if tags:
            tag_window = tk.Toplevel()
            tag_window.title("Tags")
            tag_window.geometry("200x150")

            tag_label = tk.Label(tag_window, text="Select Tag:")
            tag_label.pack()

            selected_tag = tk.StringVar()
            tag_dropdown = ttk.Combobox(tag_window, textvariable=selected_tag, values=list(tags))
            tag_dropdown.pack()

            def display_materials():
                tag = selected_tag.get()
                if tag:
                    materials = [material for material in self.materials if material.tag == tag]
                    if materials:
                        materials_window = tk.Toplevel()
                        materials_window.title(f"Materials for Tag: {tag}")
                        materials_window.geometry("400x300")

                        material_listbox = tk.Listbox(materials_window, width=60, height=10)
                        scrollbar = tk.Scrollbar(materials_window)
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                        material_listbox.config(yscrollcommand=scrollbar.set)
                        scrollbar.config(command=material_listbox.yview)

                        for material in materials:
                            material_listbox.insert(tk.END, f"Type:{material.type} Title: {material.title}  Authors: {material.authors}  Year: {material.year} Subject: {material.subject}")
                            material_listbox.bind('<<ListboxSelect>>', lambda event: self.display_material_details(event, materials))
                        material_listbox.pack()
                    else:
                        messagebox.showinfo("No Materials", f"No materials found for tag: {tag}")
                else:
                    messagebox.showinfo("No Tag Selected", "Please select a tag.")

            display_button = tk.Button(tag_window, text="Display Materials", command=display_materials)
            display_button.pack()
        else:
            messagebox.showinfo("No Tags", "No tags found in the materials.")
        tags = {}
        for material in self.materials:
            if material.tag:
                if material.tag in tags:
                    tags[material.tag].append(material)
                else:
                    tags[material.tag] = [material]
         
#----------------show recent 10 materials done ----------------------#     
# gui button 
    def run(self):
        self.root = tk.Tk()
        self.root.title("Scientific Materials Repository")
        self.root.geometry("500x350")
        
        separator_label = tk.Label(self.root)
        separator_label.grid(row=0,column= 0)        


        entry_label = tk.Label(self.root, text="Search Method:")
        entry_label.grid(row=0, column=1)
        
        self.search_option_var = tk.StringVar()
        search_option_menu = ttk.OptionMenu(self.root, self.search_option_var, "Title", "Title", "Keywords", "Authors", "Subject")
        search_option_menu.grid(row=0, column=2)
        
        self.search_entry_var = tk.StringVar()
        entry_entry = tk.Entry(self.root, textvariable=self.search_entry_var)
        entry_entry.grid(row=0, column=3)
        
        search_button = tk.Button(self.root, text="Search", command=self.search_material)
        search_button.grid(row=0, column=5)        
        
        # Advanced Search button
        advanced_search_button = tk.Button(self.root, text="Advanced Search", command=self.open_advanced_search_window)
        advanced_search_button.grid(row=1, column=5)

        self.result_frame = tk.Frame(self.root)
        self.result_frame.grid(row=4)


        add_button = tk.Button(self.root, text="Add Material", command=self.add_material)
        add_button.grid(row=2, columnspan=6)
        
        show_tag_button = tk.Button(self.root, text="Check Tags", command=self.show_tag)
        show_tag_button.grid(row=2, column=5)

        recycle_bin_button = tk.Button(self.root, text="Recycle Bin", command=self.open_recycle_bin_window)
        recycle_bin_button.grid(row=3, columnspan=6)
        
        recent_label = tk.Label(self.root, text="Recent 10 Materials")
        recent_label.grid(row=4, columnspan=6)

        self.recent_listbox = tk.Listbox(self.root, width=60, height=10)
        self.recent_listbox.grid(row=5,column=1, columnspan=6)

        # Vertical Scrollbar
        yscrollbar = tk.Scrollbar(self.root)
        yscrollbar.grid(row=5, column=8, sticky=tk.N+tk.S)
        self.recent_listbox.config(yscrollcommand=yscrollbar.set)
        yscrollbar.config(command=self.recent_listbox.yview)

        # Horizontal Scrollbar
        xscrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        xscrollbar.grid(row=6, columnspan=6, sticky=tk.E+tk.W)
        self.recent_listbox.config(xscrollcommand=xscrollbar.set)
        xscrollbar.config(command=self.recent_listbox.xview)

        # Update recent materials listbox
        self.update_recent_materials()

        self.root.mainloop()
        

#add   
class AddMaterialFrom:
    def __init__(self, window, materials, save_callback, update_recent_callback):
        self.materials = materials
        self.save_callback = save_callback
        self.update_recent_callback = update_recent_callback

        self.page_var = tk.IntVar()

        self.type_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.authors_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.abstract_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.keywords1_var = tk.StringVar()
        self.keywords2_var = tk.StringVar()
        self.keywords3_var = tk.StringVar()
        self.keywords4_var = tk.StringVar()
        self.url_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.doi_var = tk.StringVar()
        self.publisher_var = tk.StringVar()
        self.edition_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.file_path_var = tk.StringVar()

        self.window = window
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.page_var.set(1)

        self.create_first_page()

    def create_first_page(self):
        
        self.first_page_frame = tk.Frame(self.window)
        self.first_page_frame.pack(side="left", fill="both", expand=True)
        
        page_label = tk.Label(self.first_page_frame, text="Page 1")
        page_label.pack()

        title_label = tk.Label(self.first_page_frame, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(self.first_page_frame, textvariable=self.title_var, width=25)
        title_entry.pack()

        author_label = tk.Label(self.first_page_frame, text="Author(s) (you can use , to write more than one author):")
        author_label.pack()
        author_entry = tk.Entry(self.first_page_frame, textvariable=self.authors_var, width=25)
        author_entry.pack()

        typeofmaterial_label = tk.Label(self.first_page_frame, text="Type:")
        typeofmaterial_label.pack()
        typeofmaterial_entry = tk.OptionMenu(self.first_page_frame, self.type_var, "Database", "Research Paper", "Book", "Article", "Conference Paper","Other")
        typeofmaterial_entry.pack()

        year_label = tk.Label(self.first_page_frame, text="Year:")
        year_label.pack()
        year_entry = tk.Entry(self.first_page_frame, textvariable=self.year_var)
        year_entry.pack()

        month_label = tk.Label(self.first_page_frame, text="Month (Optional):")
        month_label.pack()
        month_entry = tk.Entry(self.first_page_frame, textvariable=self.month_var)
        month_entry.pack()

        day_label = tk.Label(self.first_page_frame, text="Day (Optional):")
        day_label.pack()
        day_entry = tk.Entry(self.first_page_frame, textvariable=self.day_var)
        day_entry.pack()

        subject_label = tk.Label(self.first_page_frame, text="Subject:")
        subject_label.pack()
        subject_entry = tk.Entry(self.first_page_frame, textvariable=self.subject_var, width=25)
        subject_entry.pack()

        keyword1_label = tk.Label(self.first_page_frame, text="Keyword_1 (Optional):")
        keyword1_label.pack()
        keyword1_entry = tk.Entry(self.first_page_frame, textvariable=self.keywords1_var, width=25)
        keyword1_entry.pack()

        keyword2_label = tk.Label(self.first_page_frame, text="Keyword_2 (Optional):")
        keyword2_label.pack()
        keyword2_entry = tk.Entry(self.first_page_frame, textvariable=self.keywords2_var, width=25)
        keyword2_entry.pack()

        keyword3_label = tk.Label(self.first_page_frame, text="Keyword_3 (Optional):")
        keyword3_label.pack()
        keyword3_entry = tk.Entry(self.first_page_frame, textvariable=self.keywords3_var, width=25)
        keyword3_entry.pack()

        keyword4_label = tk.Label(self.first_page_frame, text="Keyword_4 (Optional):")
        keyword4_label.pack()
        keyword4_entry = tk.Entry(self.first_page_frame, textvariable=self.keywords4_var, width=25)
        keyword4_entry.pack()       

        continue_button = tk.Button(self.first_page_frame, text="Continue", command=self.validate_first_page)
        continue_button.pack()

    def validate_first_page(self):
        title = self.title_var.get()
        authors = self.authors_var.get()
        typeofmaterial = self.type_var.get()
        year = self.year_var.get()
        month = self.month_var.get()
        day = self.day_var.get()
        subject = self.subject_var.get()
        keyword1 = self.keywords1_var.get()
        keyword2 = self.keywords2_var.get()
        keyword3 = self.keywords3_var.get()
        keyword4 = self.keywords4_var.get()

        if not title or not authors or not typeofmaterial or not year or not subject:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        try:
            year = int(year)
            current_year = datetime.now().year  # Get the current year
            if year < 1000 or year > current_year + 1 :
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid year. Please enter a valid year.")
            return
        
        try:
            if month:
                month = int(month)
                if month < 1 or month > 12:
                    raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid month. Please enter a valid month (1-12).")
            return

        try:
            if day:
                day = int(day)
                if month in [1, 3, 5, 7, 8, 10, 12]:
                    if day < 0 or day > 31:
                        raise ValueError
                elif month in [4, 6, 9, 11]:
                    if day < 0 or day > 30:
                        raise ValueError
                elif month == 2:
                    if day < 0 or day > 28:
                        raise ValueError
                else:
                    raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid day. Please enter a valid day based on the selected month.")
            return
        # Continue with the next page or save the material
        self.page_var.set(2)
        self.create_second_page()

    def go_to_next_page(self):
        self.page_var.set(2)
        self.create_second_page()

    def create_second_page(self):
        self.second_page_frame = tk.Frame(self.window)
        self.second_page_frame.pack(side="right", fill="both", expand=True)

        page_label = tk.Label(self.second_page_frame, text="Page 2: Additional Information")
        page_label.pack()

        abstract_label = tk.Label(self.second_page_frame, text="Abstract:")
        abstract_label.pack()
        self.abstract_entry = tk.Text(self.second_page_frame, height=10, width=35)
        self.abstract_entry.pack()

        typeofmaterial = self.type_var.get()

        if typeofmaterial == "Research Paper" or typeofmaterial == "Article" or typeofmaterial == "Conference Paper":
            doi_label = tk.Label(self.second_page_frame, text="DOI (Optional):")
            doi_label.pack()
            doi_entry = tk.Entry(self.second_page_frame, textvariable=self.doi_var, width=25)
            doi_entry.pack()

        elif typeofmaterial == "Book":
            publisher_label = tk.Label(self.second_page_frame, text="Publisher(Optional):")
            publisher_label.pack()
            publisher_entry = tk.Entry(self.second_page_frame, textvariable=self.publisher_var, width=25)
            publisher_entry.pack()

            edition_label = tk.Label(self.second_page_frame, text="Edition (Optional):")
            edition_label.pack()
            edition_entry = tk.Entry(self.second_page_frame, textvariable=self.edition_var, width=25)
            edition_entry.pack()

            isbn_label = tk.Label(self.second_page_frame, text="ISBN-13 (Optional):")
            isbn_label.pack()
            isbn_entry = tk.Entry(self.second_page_frame, textvariable=self.isbn_var, width=25)
            isbn_entry.pack()

        elif typeofmaterial == "Other":
            isbn_label = tk.Label(self.second_page_frame, text="ISBN-13 (Optional):")
            isbn_label.pack()
            isbn_entry = tk.Entry(self.second_page_frame, textvariable=self.isbn_var, width=25)
            isbn_entry.pack()

            doi_label = tk.Label(self.second_page_frame, text="DOI (Optional):")
            doi_label.pack()
            doi_entry = tk.Entry(self.second_page_frame, textvariable=self.doi_var, width=25)
            doi_entry.pack()

        note_label = tk.Label(self.second_page_frame, text="Note (Optional):")
        note_label.pack()
        self.note_entry = tk.Text(self.second_page_frame,height=10, width=35)
        self.note_entry.pack()

        url_label = tk.Label(self.second_page_frame, text="URL/Link (Optional):")
        url_label.pack()
        url_entry = tk.Entry(self.second_page_frame, textvariable=self.url_var, width=25)
        url_entry.pack()   

        file_button = tk.Button(self.second_page_frame, text="Upload File (Optional)", command=self.open_file_dialog)
        file_button.pack()
        self.file_entry = tk.Entry(self.second_page_frame, textvariable=self.file_path_var, width=25)  # Assign to instance variable
        self.file_entry.pack()

        submit_button = tk.Button(self.second_page_frame, text="Submit", command=self.save_material)
        submit_button.pack()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(parent=self.window)
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(tk.END, file_path)
            self.file_path_var.set(file_path)  # Update the StringVar with the selected file path
    def is_duplicate_material(self, material):
        for existing_material in self.materials:
            # Compare attributes to check for duplicates
            if (
                existing_material.title == material.title
                and existing_material.authors == material.authors
                and existing_material.year == material.year
                and existing_material.subject == material.subject
                and existing_material.type == material.type
            ):
                return True
        return False
    def save_material(self):     
        # Retrieve the entered values from the entry fields
        typeofmaterial = self.type_var.get()
        title = self.title_var.get()
        authors = self.authors_var.get()
        
        year = self.year_var.get()
        year = int(year)
        abstract = self.abstract_entry.get("1.0", tk.END)
        subject = self.subject_var.get()
        month = self.month_var.get()
        month = int(month) if month else 0
        
        day = self.day_var.get()
        day = int(day) if day else 0
        keywords_1 = self.keywords1_var.get()
        keywords_2 = self.keywords2_var.get()
        keywords_3 = self.keywords3_var.get()
        keywords_4 = self.keywords4_var.get()
          
        url = self.url_var.get()
        doi = self.doi_var.get() if typeofmaterial in ["Research Paper","Article","Conference Paper","Other"] else None
        if doi:
            if not self.validate_doi(doi):
                return        
        publisher = self.publisher_var.get() if typeofmaterial in ["Book"] else None
        edition = self.edition_var.get()  if typeofmaterial in ["Book"] else None 
        isbn = self.isbn_var.get() if typeofmaterial in ["Book","Other"] else None     
        if isbn:
            if not self.validate_isbn(isbn):
                messagebox.showinfo("Invalid ISBN", "Please enter a valid ISBN.")
                return
        
        note = self.note_entry.get("1.0", tk.END)
        file_path = self.file_entry.get()
        
        material = Material(typeofmaterial,title,authors,year,
                                 abstract, subject,month,day, keywords_1,keywords_2,keywords_3,
                                 keywords_4,url,doi,publisher,edition,isbn,note,
                                 file_path)
        
        if self.is_duplicate_material(material):
            messagebox.showinfo("Duplicate Material", "This material already exists.")
            return
    
        self.materials.append(material)
        
        

        try:
            with open('20882882materials.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([typeofmaterial,title,authors,year,
                                 abstract,subject,month,day, keywords_1,keywords_2,keywords_3,
                                 keywords_4,url,doi,publisher,edition,isbn,note,
                                 file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save material information: {e}")

        self.save_callback()
        messagebox.showinfo("Success", "Material saved successfully.")

        if self.save_callback:
            self.save_callback()

        # Update the recent materials list
        if self.update_recent_callback:
            self.update_recent_callback()

        self.on_close()
        
    def validate_doi(self, doi):
        # Check if the DOI starts with "10."
        if not doi.startswith("10."):
            messagebox.showinfo("Invalid DOI", "DOI must start with '10.'")
            return False

        return True
    def validate_isbn(self, isbn):
        # Remove any non-digit characters from the ISBN
        isbn = re.sub(r'\D', '', isbn)

        # Check the length of the ISBN
        if len(isbn) != 13:
            messagebox.showinfo("Invalid ISBN", "Please enter a 13-digit ISBN.")
            return False

        # Check the check digit
        check_digit = int(isbn[-1])
        isbn_without_check_digit = isbn[:-1]
        calculated_check_digit = self.calculate_isbn_check_digit(isbn_without_check_digit)

        if check_digit != calculated_check_digit:
            messagebox.showinfo("Invalid ISBN", "The check digit of the ISBN is incorrect.")
            return False

        return True

    def calculate_isbn_check_digit(self, isbn):
        # Calculate the check digit based on the first 12 digits of the ISBN
        check_sum = sum((3 if i % 2 == 0 else 1) * int(digit) for i, digit in enumerate(isbn))
        check_digit = (10 - (check_sum % 10)) % 10
        return check_digit

    def on_close(self):

        self.window.destroy()

#edd button
class EditForm:
    def __init__(self, material, manager):
        self.material = material
        self.manager = manager
        self.edit_window = tk.Toplevel()
        self.edit_window.title("Edit Material")
        
        # Initialize tkinter variables
        self.type_var = tk.StringVar(value=material.type)
        self.file_path_var = tk.StringVar()
        # Create and display the form
        self.create_form()

    def create_form(self):
        # Create labels, entries, and optionmenus to display the current material data
        self.form_frame = tk.Frame(self.edit_window)
        self.form_frame.pack(side="left", fill="both",expand=True)
               
        self.title_label = tk.Label(self.form_frame, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.title_entry = tk.Entry(self.form_frame)
        self.title_entry.grid(row=0, column=1)
        self.title_entry.insert(tk.END, self.material.title)

        self.author_label = tk.Label(self.form_frame, text="Author(s) (you can use , to write more than one author):")
        self.author_label.grid(row=1, column=0)
        self.author_entry = tk.Entry(self.form_frame)
        self.author_entry.grid(row=1, column=1)
        authors_str = ', '.join(self.material.authors)  # Convert list of authors to a string
        self.author_entry.insert(tk.END, authors_str)

        self.typeofmaterial_label = tk.Label(self.form_frame, text="Type:")
        self.typeofmaterial_label.grid(row=2, column=0)
        self.typeofmaterial_optionmenu = tk.OptionMenu(self.form_frame, self.type_var, *["Database", "Research Paper", "Book", "Article", "Conference Paper","Other"], command=self.reset_old_data)
        self.typeofmaterial_optionmenu.grid(row=2, column=1)

        self.year_label = tk.Label(self.form_frame, text="Year:")
        self.year_label.grid(row=3, column=0)
        self.year_entry = tk.Entry(self.form_frame)
        self.year_entry.grid(row=3, column=1)
        self.year_entry.insert(tk.END, self.material.year)

        self.month_label = tk.Label(self.form_frame, text="Month (Optional):")
        self.month_label.grid(row=4, column=0)
        self.month_entry = tk.Entry(self.form_frame)
        self.month_entry.grid(row=4, column=1)
        self.month_entry.insert(tk.END, self.material.month)

        self.day_label = tk.Label(self.form_frame, text="Day (Optional):")
        self.day_label.grid(row=5, column=0)
        self.day_entry = tk.Entry(self.form_frame)
        self.day_entry.grid(row=5, column=1)
        self.day_entry.insert(tk.END, self.material.day)

        self.subject_label = tk.Label(self.form_frame, text="Subject:")
        self.subject_label.grid(row=6, column=0)
        self.subject_entry = tk.Entry(self.form_frame)
        self.subject_entry.grid(row=6, column=1)
        self.subject_entry.insert(tk.END, self.material.subject)

        self.keyword1_label = tk.Label(self.form_frame, text="Keyword_1 (Optional):")
        self.keyword1_label.grid(row=7, column=0)
        self.keyword1_entry = tk.Entry(self.form_frame)
        self.keyword1_entry.grid(row=7, column=1)
        self.keyword1_entry.insert(tk.END, self.material.keywords1)

        self.keyword2_label = tk.Label(self.form_frame, text="Keyword_2 (Optional):")
        self.keyword2_label.grid(row=8, column=0)
        self.keyword2_entry = tk.Entry(self.form_frame)
        self.keyword2_entry.grid(row=8, column=1)
        self.keyword2_entry.insert(tk.END, self.material.keywords2)

        self.keyword3_label = tk.Label(self.form_frame, text="Keyword_3 (Optional):")
        self.keyword3_label.grid(row=9, column=0)
        self.keyword3_entry = tk.Entry(self.form_frame)
        self.keyword3_entry.grid(row=9, column=1)
        self.keyword3_entry.insert(tk.END, self.material.keywords3)

        self.keyword4_label = tk.Label(self.form_frame, text="Keyword_4 (Optional):")
        self.keyword4_label.grid(row=10, column=0)
        self.keyword4_entry = tk.Entry(self.form_frame)
        self.keyword4_entry.grid(row=10, column=1)
        self.keyword4_entry.insert(tk.END, self.material.keywords4)

        # Create a button to proceed to the second page
        self.next_button = tk.Button(self.form_frame, text="Next", command=self.goto_second_page)
        self.next_button.grid(row=11, column=0, columnspan=2)

    def reset_old_data(self, selected_type):
        if selected_type == "Research Paper" or selected_type == "Article" or selected_type == "Conference Paper":
            self.material.doi = None
        elif selected_type == "Other":
            self.material.doi = None
            self.material.isbn = None
        elif selected_type == "Book":
            self.material.isbn = None
            self.material.publisher = None
            self.material.edition = None

    def goto_second_page(self):
        # Create a new window for the second page
        self.form_frame_2 = tk.Frame(self.edit_window)
        self.form_frame_2.pack(side="right", fill="both", expand=True)

        self.abstract_label = tk.Label(self.form_frame_2, text="Abstract(Optional):")
        self.abstract_label.grid(row=0, column=0)
        self.abstract_entry = tk.Text(self.form_frame_2, height=10, width=35)
        self.abstract_entry.grid(row=0, column=1)
        self.abstract_entry.insert(tk.END, self.material.abstract)

        # Create fields based on major
        typeofmaterial = self.type_var.get()
        if typeofmaterial == "Research Paper" or typeofmaterial == "Article" or typeofmaterial == "Conference Paper":
            self.create_RACP_field()
        elif typeofmaterial == "Other":
            self.create_other_field()
        elif typeofmaterial == "Book":
            self.create_book_field()
                        
        self.note_label = tk.Label(self.form_frame_2, text="Note (Optional):")
        self.note_label.grid(row=1, column=0)
        self.note_entry = tk.Text(self.form_frame_2, height=10, width=35)
        self.note_entry.grid(row=1, column=1)
        self.note_entry.insert(tk.END, self.material.note)
        
        self.url_label = tk.Label(self.form_frame_2, text="URL/ Link (Optional):")
        self.url_label.grid(row=2, column=0)
        self.url_entry = tk.Entry(self.form_frame_2, width=25)
        self.url_entry.grid(row=2, column=1)
        self.url_entry.insert(tk.END, self.material.url)
        
        self.file_button = tk.Button(self.form_frame_2, text="Open File",command=self.open_file_dialog)
        self.file_button.grid(row=3, column=0)
        self.file_entry = tk.Entry(self.form_frame_2, textvariable=self.file_path_var, width=35)
        self.file_entry.grid(row=3, column=1)
        self.file_entry.insert(tk.END, self.material.file_path)
        
        # Create a save button
        self.save_button = tk.Button(self.form_frame_2, text="Save", command=self.update_material)
        self.save_button.grid(row=8, column=0, columnspan=2)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(tk.END, file_path)
            self.file_path_var.set(file_path)  # Update the StringVar with the selected file path
    def create_RACP_field(self):
        # Initialize tkinter variable
        self.doi_var = tk.StringVar(value=self.material.doi)    
        self.doi_label = tk.Label(self.form_frame_2, text="DOI (Optional):")
        self.doi_label.grid(row=4, column=0)
        self.doi_entry = tk.Entry(self.form_frame_2,textvariable=self.doi_var)
        self.doi_entry.grid(row=4, column=1)
        
    def create_other_field(self):
        # Initialize tkinter variable
        self.doi_var = tk.StringVar(value=self.material.doi)
        self.doi_label = tk.Label(self.form_frame_2, text="DOI (Optional):")
        self.doi_label.grid(row=4, column=0)
        self.doi_entry = tk.Entry(self.form_frame_2,textvariable=self.doi_var)
        self.doi_entry.grid(row=4, column=1)        
        self.isbn_var = tk.StringVar(value=self.material.isbn)
        self.isbn_label = tk.Label(self.form_frame_2, text="ISBN-13 (Optional):")
        self.isbn_label.grid(row=5, column=0)
        self.isbn_entry = tk.Entry(self.form_frame_2,textvariable=self.isbn_var)
        self.isbn_entry.grid(row=5, column=1)
        
    def create_book_field(self):
        # Initialize tkinter variable
        self.publisher_var = tk.StringVar(value=self.material.publisher)
        self.publisher_label = tk.Label(self.form_frame_2, text="Publisher (Optional):")
        self.publisher_label.grid(row=4, column=0)
        self.publisher_entry = tk.Entry(self.form_frame_2,textvariable=self.publisher_var)
        self.publisher_entry.grid(row=4, column=1)
        
        self.edition_var = tk.StringVar(value=self.material.edition)
        self.edition_label = tk.Label(self.form_frame_2, text="Edition(Optional):")
        self.edition_label.grid(row=5, column=0)
        self.edition_entry = tk.Entry(self.form_frame_2,textvariable=self.edition_var)
        self.edition_entry.grid(row=5, column=1)
        
        self.isbn_var = tk.StringVar(value=self.material.isbn)
        self.isbn_label = tk.Label(self.form_frame_2, text="ISBN-13 (Optional):")
        self.isbn_label.grid(row=6, column=0)
        self.isbn_entry = tk.Entry(self.form_frame_2,textvariable=self.isbn_var)
        self.isbn_entry.grid(row=6, column=1)
        
    def update_material(self):
        
        self.material.type = self.type_var.get()
        self.material.title = self.title_entry.get()
        authors_str = self.author_entry.get()
        self.material.authors = [author.strip() for author in authors_str.split(',')]  
        year = self.year_entry.get()
        try:
            year = int(year)
            current_year = datetime.now().year  # Get the current year
            if year < 1000 or year > current_year:
               raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid year. Please enter a valid year.")
            return
        self.material.year = year  # Assign the valid year
              
        self.material.abstract = self.abstract_entry.get("1.0", tk.END)
        self.material.subject = self.subject_entry.get()
        
        month = self.month_entry.get()
        if month:
            try:
                month = int(month)
                if month < 0 or month > 12:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid month. Please enter a valid month (1-12).")
                return
            self.material.month = month  # Assign the valid month
            
        day = self.day_entry.get()
        if day:
            try:
                day = int(day)
                month = int(month)  # convert month to an integer for comparison
                if (month in [1, 3, 5, 7, 8, 10, 12] and (day < 0 or day > 31)) or \
                (month in [4, 6, 9, 11] and (day < 0 or day > 30)) or \
                (month == 2 and (day < 0 or day > 28)):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid day. Please enter a valid day based on the selected month.")
                return
                    
            self.material.day = day  # Assign the valid day
        
        self.material.keywords1 = self.keyword1_entry.get()
        self.material.keywords2 = self.keyword2_entry.get()
        self.material.keywords3 = self.keyword3_entry.get()
        self.material.keywords4 = self.keyword4_entry.get()
        
        self.material.url = self.url_entry.get() 
        self.material.file_path = self.file_entry.get()
              
        doi = self.doi_var.get() if hasattr(self, 'doi_var') else None
        if doi and not doi.startswith("10."):
            messagebox.showerror("Invalid DOI", "DOI must start with '10.'")
            return
        self.material.doi = doi
        self.material.publisher = self.publisher_var.get() if hasattr(self, 'publisher_var') else None
        self.material.edition = self.edition_var.get() if hasattr(self, 'edition_var') else None
        self.material.isbn = self.isbn_var.get() if hasattr(self, 'isbn_var') else None

        self.material.note = self.note_entry.get("1.0", tk.END)

        # Save the updated material list to the CSV file
        self.manager.save_to_csv()

        # Close the edit windows
        self.edit_window.destroy()

        # Display a message box to confirm the update
        messagebox.showinfo("Update Successful", "The material information has been updated.")

      
class RecycleBin:
    def __init__(self, window, material_manager):  # Accept the MaterialManager instance
        self.window = window
        self.material_manager = material_manager  # Save the MaterialManager instance
        self.recycle_bin_filename = "20882882recycle_bin.csv"
        self.data = self.read_recycle_bin_csv()

    def read_recycle_bin_csv(self):
        try:
            with open(self.recycle_bin_filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = list(reader)
            return data
        except FileNotFoundError:
            return []

    def delete_selected_item(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this material?")
            if confirmation:
                del self.data[selected_index[0]]
                listbox.delete(selected_index[0])
                self.save_data_to_recycle_bin_csv()  # Updated method name
                messagebox.showinfo("Deletion Successful", "The selected item has been deleted.")
        else:
            messagebox.showinfo("Deletion Cancelled", "No item selected for deletion.")

    def restore_selected_item(self, listbox):  # Remove the material_manager parameter
        selected_index = listbox.curselection()
        if selected_index:
            confirmation = messagebox.askyesno("Confirm Restoration", "Are you sure you want to restore this item?")
            if confirmation:
                restored_data = self.data[selected_index[0]]
                self.material_manager.restore_material(restored_data)  # Use the MaterialManager instance saved in __init__
                listbox.delete(selected_index[0])
                self.data.pop(selected_index[0])  # Remove the restored item from the recycle bin data
                self.save_data_to_recycle_bin_csv()
                messagebox.showinfo("Restoration Successful", "The selected item has been restored.")
        else:
            messagebox.showinfo("Restoration Cancelled", "No item selected for restoration.")

    def save_data_to_recycle_bin_csv(self):  # Updated method name
        with open(self.recycle_bin_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
            
            

    def show_recycle_bin_window(self):
        self.window.title("Recycle Bin")

        listbox = tk.Listbox(self.window, width=60, height=15)
        scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        for item in self.data:
            display_text = f"Type: {item[0]}, Title: {item[1]}, Authors: {item[2]} Subject: {item[5]}"
            listbox.insert(tk.END, display_text)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        delete_button = tk.Button(self.window, text="Delete", command=lambda: self.delete_selected_item(listbox))
        material_manager = MaterialManager(filename="20882882materials.csv")
        restore_button = tk.Button(self.window, text="Restore", command=lambda: self.restore_selected_item(listbox))

        delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        restore_button.pack(side=tk.LEFT, padx=5, pady=5)


if __name__ == "__main__":
    
    manager = MaterialManager("20882882materials.csv")
    
    manager.run()
    