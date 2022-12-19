#!/usr/bin/env python
# coding: utf-8

# # Basic Plotly Charts

# ## Objectives
# 
# In this lab, you will learn about creating plotly charts using plotly.graph_objects and plotly.express.
# 
# Learn more about:
# 
# *   [Plotly python](https://plotly.com/python/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDV0101ENSkillsNetwork20297740-2021-01-01)
# *   [Plotly Graph Objects](https://plotly.com/python/graph-objects/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDV0101ENSkillsNetwork20297740-2021-01-01)
# *   [Plotly Express](https://plotly.com/python/plotly-express/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDV0101ENSkillsNetwork20297740-2021-01-01)
# *   Handling data using [Pandas](https://pandas.pydata.org/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDV0101ENSkillsNetwork20297740-2021-01-01)
# 
# #### Airline Reporting Carrier On-Time Performance Dataset
# 
# The Reporting Carrier On-Time Performance Dataset contains information on approximately 200 million domestic US flights reported to the United States Bureau of Transportation Statistics. The dataset contains basic information about each flight (such as date, time, departure airport, arrival airport) and, if applicable, the amount of time the flight was delayed and information about the reason for the delay. This dataset can be used to predict the likelihood of a flight arriving on time.
# 
# Preview data, dataset metadata, and data glossary [here.](https://dax-cdn.cdn.appdomain.cloud/dax-airline/1.0.1/data-preview/index.html)

# In[1]:


# Import required libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ### Read Data

# In[2]:


url = '/Users/QXJ/Desktop/IBM/Data visualization/airline_data.csv'
pd.set_option('display.max_columns', None)
df = pd.read_csv(url,index_col = False)
df.head()


# In[3]:


df.shape


# In[4]:


df = df[['Year', 'Quarter', 'Month','FlightDate','Reporting_Airline','OriginState','DestState','DepTime','ArrTime','DepDelay','ArrDelay','Distance','DistanceGroup','Flights']]


# In[5]:


df.head()


# In[6]:


df.columns


# In[7]:


# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = df.sample(n=500, random_state=42)


# In[8]:


data.shape


# ### Structure
# 
# #### plotly.graph_objects
# 
# 1.  Scatter plot 
# 
#     Theme: How departure time changes with respect to airport distance
# 
# 2.  - Line plot
# 
#     Theme: Extract average monthly delay time and see how it changes over the year
# 
# #### plotly.express
# 
# 1.  Bar chart 
# 
#     Theme: Extract number of flights from a specific airline that goes to a destination
# 
# 2.  Bubble chart
# 
#     Theme: Get number of flights as per reporting airline
# 
# 3.  Histogram
# 
#     Theme: Get distribution of arrival delay
# 
# 4.  Pie chart
# 
#     Theme: Proportion of distance group by month (month indicated by numbers)
# 
# 5.  Sunburst chart
# 
#     Theme: Hierarchical view in othe order of month and destination state holding value of number of flights
# 

# ## plotly.graph_objects

# ### 1. Scatter plot

# In[9]:


# First we create a figure using go.Figure and adding trace to it through go.scatter
fig = go.Figure(data=go.Scatter(x=data['Distance'], y=data['DepTime'], mode='markers', marker=dict(color='red')))
# Updating layout through `update_layout`. Here we are adding title to the plot and providing title to x and y axis.
fig.update_layout(title='Distance vs Departure Time', xaxis_title='Distance', yaxis_title='DepTime')
# Display the figure
fig.show()


# ![image.png](attachment:image.png)

# ### 2. Line chart

# In[10]:


# Extract average monthly arrival delay time and see how it changes over the year
df_month = data.groupby('Month')['ArrDelay'].mean().reset_index()
df_month


# In[37]:


# First we create a figure using go.Figure and adding trace to it through go.scatter
fig = go.Figure(data=go.Scatter(x=df_month['Month'], y=df_month['ArrDelay'], mode='lines', marker=dict(color='green')))
# Updating layout through `update_layout`. Here we are adding title to the plot and providing title to x and y axis.
fig.update_layout(title='Average arrival delay by month', xaxis_title='Month', yaxis_title='Arrival delay')
# Display the figure
fig.show()


# ![image.png](attachment:image.png)

# ## Plotly.express

# ### 1. Bar Chart

# In[18]:


# Compute total number of flights in each combination of destinatoin 
df_dest = data.groupby('DestState')['Flights'].sum().reset_index()
df_dest.head()


# In[20]:


fig = px.bar(df_dest, x="DestState", y="Flights", title='Total number of flights to the destination state split by reporting airline') 
fig.show()


# ![image.png](attachment:image.png)

# ### 3. Bubble chart

# In[22]:


# Group the data by reporting airline and get number of flights
df_reporting = data.groupby('Reporting_Airline')['Flights'].sum().reset_index()
df_reporting.head()


# In[29]:


fig = px.scatter(df_reporting, x="Reporting_Airline", y="Flights", size='Flights',hover_name='Reporting_Airline', title='Reporting airline vs. Total number of flights') 
fig.show()


# ![image.png](attachment:image.png)

# ### 3. Histogram

# In[30]:


# Set missing values to 0
data['ArrDelay'] = data['ArrDelay'].fillna(0)


# In[33]:


fig = px.histogram(data,x='ArrDelay')
fig.show()


# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# ### 4. Pie chart

# In[34]:


fig = px.pie(data, values='Month', names='DistanceGroup', title='Distance group proportion by month')
fig.show()


# ![image.png](attachment:image.png)

# ### 5. Sunburst chart*
# 
# *Idea: Hierarchical view in othe order of month and destination state holding value of number of flights*

# In[36]:


fig = px.sunburst(data, path=['Month', 'DestState'], values='Flights')
fig.show()


# ![image.png](attachment:image.png)

# In[ ]:




