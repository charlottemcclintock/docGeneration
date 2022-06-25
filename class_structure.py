

# import modules
import pyodbc 
import textwrap

'''
Viz - basic structure of classes for visualization scripts
'''
class Viz():

    def __init__(self):

        # add database connection as attribute to centralize
        self.cnxn = pyodbc.connect("Driver={None};"
                    "Server=None;"
                    "Database=None;"
                    "Trusted_Connection=yes;")
        
        # color palette 
        self.colors = {}
                    
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

    def wrap_labels(self, ax, width, break_long_words=False):
        labels = []
        for label in ax.get_yticklabels():
            text = label.get_text()
            labels.append(textwrap.fill(text, width=width,
                        break_long_words=break_long_words))
        ax.set_yticklabels(labels, rotation=0)
    
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
