import tkinter as tk
from tkinter import ttk

from display_data import *
from search import *
from data_helper import *

from pandastable import Table, TableModel
import bargraph
import matplotlib


matplotlib.use("TkAgg")

#Reusable font sizes
LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Open Sans", 20)
SMALL_FONT = ("Open Sans", 15)


# Main Window
class WelcomeWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (SelectOptions, ViewCharts, ViewSummary):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(SelectOptions)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Select Options Window
class SelectOptions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.createLabels()
        self.createButtons(controller)

    def createLabels(self):
        header = tk.Label(self, text="HDB Resale Flats Analyser", font=LARGE_FONT)
        label = tk.Label(self,
                         text="This service enables you to check the resale flat prices within the last 3 years based on regions, "
                              "towns and flat-types.",
                         font=SMALL_FONT, wraplength=450)
        header.pack(padx=0, pady=20)
        label.pack(padx=10, pady=10)

    def createButtons(self, controller):
        chartsBTN = tk.Button(self, text="View Charts", height=5, width=30, font=SMALL_FONT,
                              command=lambda: controller.show_frame(ViewCharts))
        chartsBTN.pack(pady=10, padx=10)
        summaryBTN = tk.Button(self, text="View Summary", height=5, width=30, font=SMALL_FONT,
                               command=lambda: controller.show_frame(ViewSummary))
        summaryBTN.pack()

# Export Data Window
class ExportResults(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = ViewExportSummary(container, self)
        self.frames[ViewExportSummary] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ViewExportSummary)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Hanyi Function
class ViewCharts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Analyse Resale Flats by Region", font=NORM_FONT)
        label.pack(padx=10, pady=10)

        backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack(padx=10, pady=10)


# Kah En Function
class ViewSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Overview of Resale Flats Prices", font=NORM_FONT)
        label.pack(pady=10, padx=10)
        backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack(padx=5, pady=5)


        #get towns, regions,flatTypes data from csv
        global df
        df = data_helper.get_dataframe()
        towns = data_helper.get_all_towns()
        regions = data_helper.get_all_regions()
        flatTypes = data_helper.get_all_flatTypes()


        selectionlabel = tk.Label(self, text="Please select an option for regions, towns and flat types", font=SMALL_FONT)
        selectionlabel.pack(padx=20, pady=20)
        # Setting values for regions combo box
        listofRegions = sorted(regions)
        self.comboBoxRegion = ttk.Combobox(self, state="readonly")
        self.comboBoxRegion.pack(padx=5, pady=5)
        self.comboBoxRegion.bind('<<ComboboxSelected>>', lambda x: self.updateComboBox("region"))
        self.comboBoxRegion['values'] = ["Select Region"]+listofRegions
        self.comboBoxRegion.current(0)

        # Setting values for town combo box
        listofTowns = sorted(towns)
        self.comboBoxTown = ttk.Combobox(self, state="readonly")
        self.comboBoxTown.pack(padx=5, pady=5)
        self.comboBoxTown.bind('<<ComboboxSelected>>', lambda x: self.updateComboBox(""))
        self.comboBoxTown['values'] = ["Select Town"]+listofTowns
        self.comboBoxTown.current(0)


        # Setting values for flat types combo box
        listofFlatTypes = sorted(flatTypes)
        self.comboxBoxFlatTypes = ttk.Combobox(self, state="readonly")
        self.comboxBoxFlatTypes.pack(padx=5, pady=5)
        self.comboxBoxFlatTypes['values'] = ["Select Flat Type"]+listofFlatTypes
        # self.comboxBoxFlatTypes.set("Select Flat Type")
        self.comboxBoxFlatTypes.current(0)

        topframe = tk.Frame(self)
        topframe.pack(side=tk.TOP)

        filter = tk.Button(self, text="Filter", font=SMALL_FONT,
                                 command=lambda: self.updateTable(topframe))
        filter.pack(padx=10, pady=10)

        #Creating table for summary
        global frame
        frame = tk.Frame(self)
        frame.pack()
        self.table = Table(frame, dataframe=df,showstatusbar=True)
        self.table.show()

        exportButton = tk.Button(self, text="Export Results", font=SMALL_FONT,
                                command=lambda: self.displayExport())
        exportButton.pack(padx=10, pady=10)



    #resets town dropdown based on region
    def updateComboBox(self,control):
        if control == "region":
            listofTowns = get_town_acrd_region(self.comboBoxRegion.get())
            self.comboBoxTown['values'] = listofTowns
            self.comboBoxTown.current(0)

    def updateTable(self,topframe):

        for child in topframe.winfo_children():
            child.destroy()


        if not self.comboBoxRegion.get() == "Select Region" or self.comboBoxTown.get() == "Select Town" or self.comboxBoxFlatTypes == "Select Flat Type":
            label = tk.Label(self, text="Your Results",
                             font=NORM_FONT)
            label.pack(padx=20, pady=20)

            regionLabel = tk.Label(topframe, text="Region:" + self.comboBoxRegion.get())
            regionLabel.pack()
            townLabel = tk.Label(topframe, text="Town:" + self.comboBoxTown.get())
            townLabel.pack()
            flatLabel = tk.Label(topframe,text="Flat Type:" +  self.comboxBoxFlatTypes.get())
            flatLabel.pack()
        else:
            label = tk.Label(topframe, text="Search keywords are empty",
                             font=SMALL_FONT)
            label.pack(padx=20, pady=20)

        #repopulate dictionary for table based on new selected drop down value
        filters = {"town": self.comboBoxTown.get(), "flat_type": self.comboxBoxFlatTypes.get()}
        # Replace default values to ""
        for item in filters:
            if filters[item] == "Select Town" or filters[item] == "Select Flat Type":
                filters[item] = ""

        #filtered df
        valuesBasedOnFilters = get_filtered_data(filters)
        #repopulate table with filtered data
        self.table.updateModel(TableModel(valuesBasedOnFilters))
        self.table.redraw()


    def displayExport(self):
        mainApp = ExportResults()
        mainApp.title("Export Results")
        mainApp.geometry("800x800")
        mainApp.mainloop()



# Kah En Function
class ViewExportSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Export your results", font=NORM_FONT)
        label.pack(pady=10, padx=10)

        regions = data_helper.get_all_regions()

        # Setting values for regions combo box
        listofRegions = sorted(regions)
        self.comboBoxRegion = ttk.Combobox(self, state="readonly")
        self.comboBoxRegion.pack(pady=0, padx=0)
        self.comboBoxRegion.bind('<<ComboboxSelected>>', lambda x: self.updateComboBox("region"))
        self.comboBoxRegion['values'] = ["Select Region"] + listofRegions
        self.comboBoxRegion.current(0)


app = WelcomeWindow()
app.title("HDB Resale Flats Analyser")
app.geometry("900x700")
app.mainloop()
