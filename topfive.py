
# import modules
import pyodbc 
import pandas as pd 
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
import textwrap
from matplotlib.lines import Line2D


# import class structure to use common functionality
from class_structure import Viz

class TopFive(Viz):
    
    def __init__(self, place): 

        # run init from parent class
        super().__init__()
        
        # set mission
        self.place = place

        # run everything 
        self.runMethods()

    def queryData(self):
        '''
        Query data from SQL, format query with place. 
        '''

        # define formattable query
        query = '''OMITTED'''

        # format sql statement and query data 
        mission_query = query.format("'"+ self.place + "'")
        data = pd.read_sql(mission_query, self.cnxn)

        return data


    def preprocessData(self, data, ):

        '''
        Clean and preprocess data, write out useful objects. 
        '''
        # drop rows with null scores
        data = data[~data['Score'].isnull()]

        # for multi-part places
        if len(pd.unique(data['Part'])) > 1:

            # calculated averages across [place
            groups = data.groupby('Name')
            grouped_avgs = []

            for name, group_df in groups: 
                # mission average and total responses
                group_sum = sum(group_df['Score'] * group_df['Count of Respondents'])
                total_responses = sum(group_df['Count of Respondents'])
                group_avg = group_sum/total_responses
                # store in dict
                group_dict = {'Cost Center Name': name, 
                'Score': group_avg, 
                'Count of Respondents': total_responses, 
                'Section': pd.unique(group_df['Section'])[0], 
                'Comparison Score': pd.unique(group_df['Comparison Score'])[0]}
                grouped_avgs.append(group_dict)

            data = pd.DataFrame(grouped_avgs)

        # sort values and reset index 
        data = data.sort_values('Satisfaction Score', ascending=False)
        data = data.reset_index()

        # subset top and bottom
        top5 = data.head(5).copy()
        bottom5 =  data.tail(5).copy()

        # add ordered sequence for annotation
        top5.loc[:,'AnnotationOrder'] = [0, 1, 2, 3, 4]
        bottom5.loc[:,'AnnotationOrder'] = [0, 1, 2, 3, 4]

        return top5, bottom5

    def visualizeFigure(self, top5, bottom5):
        '''
        Create visualization in matplotlib, render, and save.
        '''

        # set up figure
        fig, axs = plt.subplots(ncols=2, sharex=False, figsize=(10, 4))

        # top 5 - points colored by section, grey triangles for regional avg
        sns.pointplot(y="Name", x="Comparison Score",  
                    data=top5, ax=axs[0], color='grey', join=False, markers='^')
        sns.pointplot(y="Name", x="Score",  hue='Section',
                    data=top5, ax=axs[0], join=False, palette=self.colors)
        # bottom 5 - points colored by section, grey triangles for regional avg
        sns.pointplot(y="Name", x="Comparison Score",  
                    data=bottom5, ax=axs[1], color='grey', join=False, markers='^')
        sns.pointplot(y="Name", x="Score",  hue='Section',
                    data=bottom5, ax=axs[1], join=False, palette=self.colors)

        # set flexible lower bound depending on mission scores
        if min(bottom5['Satisfaction Score']) - 1 > 0:
            lower_bound = min(bottom5['Satisfaction Score']) - 1
        else: 
            lower_bound = 0
        
        # add labels
        axs[0].set(xlabel='Average Score', 
                    ylabel=None, xlim=(lower_bound, 5), title='Top 5 Cost Centers')
        axs[1].set(xlabel='Average Score', 
                    ylabel=None, xlim=(lower_bound, 5), title='Bottom 5 Cost Centers')


        # methods to apply to both plots
        for i in [0,1]:

            # remove legends since we're annotating the points with section
            axs[i].get_legend().remove()

            # set grid below points
            axs[i].grid(b=True)
            axs[i].set_axisbelow(True)

            # remove spines 
            axs[i].spines['left'].set_visible(False)
            axs[i].spines['right'].set_visible(False)
            axs[i].spines['top'].set_visible(False)

            # annotate both axes
            df_list = [top5, bottom5]
            for index, row in df_list[i].iterrows():
                # annotate points with score and section
                label_text = f'''{str(round(row['Score'], 1))} ({row['Section']})'''
                axs[i].text(s=label_text, y=row['AnnotationOrder']-0.25, x=row['Score'], 
                        ha='center', fontsize=8)
                # 
                axs[i].text(s=str(int(row['Count of Respondents'])) + ' responses', 
                        y=row['AnnotationOrder'], x=5.1, ha='left', fontsize=8, 
                        va='center')
                
                self.wrap_labels(axs[i], 15)


        legend_elements = [Line2D([0], [0], marker='^', color='white', 
                            label='Comparison Average', markerfacecolor='grey', 
                            markersize=11),
                            Line2D([0], [0], marker='o', color='white', 
                            label='Average', markerfacecolor='grey', 
                            markersize=11)]

        axs[1].legend(handles=legend_elements, bbox_to_anchor=(0.2, -0.28), 
                        loc='lower left', ncol=2)

        # adjust spacing, add title, save, and show
        plt.subplots_adjust(top=0.85, wspace=1.1, hspace=1.1)
        plt.suptitle(f'Plot Title')
        plt.savefig(f'../test_examples/{self.place}/plot.png', bbox_inches = "tight")
        plt.show()

    def writeDescriptions(self, top5, bottom5):
      
      desc_fig = 'Description of figure \n\n'

        # top and bottom sections and counts
        top_sections, top_counts = top5['Section'].value_counts().index.tolist(), top5['Section'].value_counts().values.tolist()
        bottom_sections, bottom_counts = bottom5['Section'].value_counts().index.tolist(), bottom5['Section'].value_counts().values.tolist()
            # list sections and services together in a single string
        top_string_list = [f'{section} ({count})' for section, count in zip(top_sections, top_counts)]
        bottom_string_list = [f'{section} ({count})' for section, count in zip(bottom_sections, bottom_counts)]
        # format into string
        desc_top_sections = f'Sections in the top five include {self.list_syntax(top_string_list)}. '
        desc_bottom_sections = f'Sections in the bottom five include {self.list_syntax(bottom_string_list)}. '


        # list top and bottom services, percent compliance, targets
        top_services, top_scores = top5['Name'].tolist(), top5['Score'].tolist()
        bottom_services, bottom_scores = bottom5['Name'].tolist(), bottom5['Score'].tolist()
        top_scores = [round(i, 1) for i in top_scores]
        bottom_scores = [round(i, 1) for i in bottom_scores]

        # format into string - alt + z to wrap text (cleaner way to do this?)
        desc_top_services = f'The top overall service by score was {top_services[0]} ({top_scores[0]}), followed by {top_services[1]} ({top_scores[1]}),  {top_services[2]} ({top_scores[2]}),  {top_services[3]} ({top_scores[3]}) and {top_services[4]} ({top_scores[4]}).'
        desc_bottom_services = f'The bottom overall service by score was {bottom_services[4]} ({bottom_scores[4]}), followed by {bottom_services[3]} ({bottom_scores[3]}),  {bottom_services[2]} ({bottom_scores[2]}),  {top_services[1]} ({bottom_scores[1]}), and {bottom_services[0]} ({bottom_scores[0]}).'

        full_text = desc_fig + desc_top_sections + desc_top_services + '\n\n' + desc_bottom_sections + desc_bottom_service
        
        # write descriptive text as text
        with open(f"../test_examples/{self.place}/top.txt","w+") as f:
            f.write(full_text + '\n')
            
        print('Wrote descriptive text:')
        print(full_text)

    def runMethods(self):
        data = self.queryData()
        top5, bottom5 = self.preprocessData(data)
        self.visualizeFigure(top5, bottom5)
        self.writeDescriptions(top5, bottom5)

if __name__ == "__main__":
    instance = TopFive(place = "Place")


