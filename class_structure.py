
# import modules
import pyodbc 
import textwrap

class Viz():
    '''
    Parent class laying out basic structure of classes for visualization scripts
    and containing helpful methods/attributes across scripts. 
    '''

    def __init__(self):

        '''
        Define attributes shared across classes, including database connection, 
        color palettes.
        '''

        # add database connection as attribute to centralize
        self.cnxn = pyodbc.connect("Driver={None};"
                    "Server=None;"
                    "Database=None;"
                    "Trusted_Connection=None;")
        
        # color palette for sections
        self.colors = {"1":"#76B7B2",
                            "2":"#663c63",
                            "3":"#F28E2B",
                            "4":"#EDC948",
                            "5":"#59A14F",
                            "6":"#E15759",
                            "7":"#034214",
                            "8":"#4E79A7"}

    '''
    General structure of visualization scripts
        queryData
        preprocessData
        visualizeFigure
        writeDescriptions
        runMethods
    '''
    def queryData(): 
        pass    

    def preprocessData(): 
        pass

    def visualizeFigure(): 
        pass

    def writeDescriptions(): 
        pass

    def runMethods():
        pass

    '''
    Define some helpful functions
        wrap_labels
        list_syntax
        query_mission_name
    '''

    # wrap y labels in axis text
    def wrap_labels(self, ax, width, break_long_words=False):
        labels = []
        for label in ax.get_yticklabels():
            text = label.get_text()
            labels.append(textwrap.fill(text, width=width,
                        break_long_words=break_long_words))
        ax.set_yticklabels(labels, rotation=0)
    
    # get english grammar syntax string back from a list of any length
    def list_syntax(self, string_list):
        if len(string_list) > 2:
            rm_string = ', '.join(string_list)
            rm_string = ', and '.join(rm_string.rsplit(', ', 1))
            return f"""{rm_string}"""
        elif len(string_list) == 2: 
            return f"""{string_list[0]} and {string_list[1]}"""
        elif len(string_list) == 1: 
            return f"""{string_list[0]}"""
        elif len(string_list) == 0:
            return ''
    
    # add in two single quotes to query name if place name has quotes (e.g. Cote d'Ivoire)
    def query_place_name(self, name):
        if "'" in name:
            return name.replace("'", "''")
        else: 
            return name
