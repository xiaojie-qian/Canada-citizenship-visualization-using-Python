#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip3 install dash')


# In[7]:


get_ipython().system('pip3 install httpx==0.20 dash plotly')


# In[8]:


import pandas as pd
import plotly.express as px
import dash


# In[6]:


import dash_core_components as dcc
import dash_html_components as html


# ### 1. Data preparation

# In[10]:


# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})


# In[11]:


data = airline_data.sample(n=500, random_state=42)


# In[12]:


data.shape


# In[13]:


data.head()


# In[15]:


fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')
fig.show()


# ### 2. Create dash application and get the layout skeleton

# In[ ]:


# Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('Airline Dashboard'),
                                style={'textAlign': 'center', 
                                       'color': '#503D36', 'font-size': 40}
                                html.P('Proportion of distance group (250 mile distance interval group) by flights.', 
                                       style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig),

                    ])

# Run the application                   
if __name__ == '__main__':
    app.run_server()


# # run the code in the terminal
# python3 dash_basics.py
# # stop the running application 
# Press ctrl+c inside the terminal to stop the dash application.

# ![image.png](attachment:image.png)

# In[ ]:




