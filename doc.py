
# import modules
import docx
from docx.shared import Pt
from docx.shared import Inches
import os
import glob
import pyodbc
import pandas as pd

class BuildDocument(): 

    def __init__(self, place):

        # add mission as attribute
        self.place = place

        # run method below 
        self.getPlaceInfo()
        self.importText()
        self.buildDocument()


    def getPlaceInfo(self):

        # database connection class
        cnxn = pyodbc.connect("None};"
            "Server=None;"
            "Database=None;"
            "Trusted_Connection=yes;")

        # define query to get USS compliance by service type
        query = ''''''

        # format sql statement and query data 
        mission_query = query.format("'"+ self.place + "'")
        overview = pd.read_sql(place_query, cnxn)
        
        # save post info into class attribute
        self.overview = overview

    def importText(self):

        # list of paths to both specific and standard text
        specific_text = glob.glob(os.path.join(os.getcwd(), "..", "test_examples", self.place, "*.txt"))
        standard_text = glob.glob(os.path.join(os.getcwd(),  "standard_text", "*.txt"))
        all_text = specific_text + standard_text

        # create dict with section names and text sections
        text_sections = dict()
        for file_path in all_text:
            # clean section name from file name
            section = os.path.basename(file_path)
            section = section.replace('.txt', '')
            # add each file to dictionary section
            with open(file_path) as f_input:
                text_sections.update({section: f_input.read()})

        self.text_sections = text_sections

    def buildDocument(self):

        # instantiate document class
        doc = docx.Document()

        # add bold line
        def add_bold_line(text):
            bold_text = doc.add_paragraph()
            bold_text.add_run(text).bold=True

        # define some methods to shorten and simplify script
        # add bold, uppercase header
        def add_header(text): 
            header = doc.add_paragraph()
            header.add_run(text.upper()).bold=True
        # add italic, uppercase subheader
        def add_subheader(text): 
            header = doc.add_paragraph()
            header.add_run(text.upper()).italic=True
        # add figure from mission folder, pass in name and width
        def add_figure(name, width):
            doc.add_picture(f'../test_examples/{self.place}/{name}.png', width=Inches(width))

        # set overall fonts
        font = doc.styles['Normal'].font
        font.name = 'Times New Roman'

        # set up intro for document
        add_bold_line('TO:')
        add_bold_line('THROUGH:')
        add_bold_line('FROM:')

        # add horizontal line break
        doc.add_paragraph('________________________________________________________________________')

        # add introduction header
        add_header('Introduction')
        # add standard introduction text, format with region/oe score
        doc.add_paragraph(self.text_sections['intro'].format(self.overview['Region'][0], self.overview['Score'][0]))

        # overview section
        add_header('Overview')
        doc.add_paragraph(self.text_sections['timeseries'])
        add_figure('timeseries', 5.5)

        # top 5/bottom 5 - uss
        add_header('Top & Bottom Services')
        doc.add_paragraph(self.text_sections['topfive'])
        add_figure('top5bottom5-uss', 6)

        # page break for appendix
        doc.add_page_break()
        add_header('Appendix')
        doc.add_paragraph('')

        # write out document
        doc.save(f'../test_examples/{self.place}/demo-{self.place}.docx')
        print('Wrote out document.')


if __name__ == "__main__":
    instance = BuildDocument(place='Place')


