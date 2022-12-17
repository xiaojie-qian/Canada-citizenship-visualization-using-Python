#!/usr/bin/env python
# coding: utf-8

# # Generating Maps

# # Choropleth Maps <a id="8"></a>
# 
# A `Choropleth` map is a thematic map in which areas are shaded or patterned in proportion to the measurement of the statistical variable being displayed on the map, such as population density or per-capita income. The choropleth map provides an easy way to visualize how a measurement varies across a geographic area, or it shows the level of variability within a region. Below is a `Choropleth` map of the US depicting the population by square mile per state.
# 
# <img src = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%205/images/2000_census_population_density_map_by_state.png" width = 600> 

# ### Datasets:
# 
# Immigration to Canada from 1980 to 2013 - [International migration flows to and from selected countries - The 2015 revision](http://www.un.org/en/development/desa/population/migration/data/empirical2/migrationflows.shtml?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDV0101ENSkillsNetwork20297740-2021-01-01) from United Nation's website. The dataset contains annual data on the flows of international migrants as recorded by the countries of destination. The data presents both inflows and outflows according to the place of birth, citizenship or place of previous / next residence both for foreigners and nationals. For this lesson, we will focus on the Canadian Immigration data
# 

# In[52]:


pip install folium


# In[2]:


import numpy as np
import pandas as pd 
import folium as fo
import json


# In[3]:


filepath = r"C:\Users\QXJ\Desktop\IBM\Data visulization\Canada_clean.csv" 
df = pd.read_csv(filepath, index_col = False)


# In[4]:


df.head()


# In[8]:


df.shape


# In[5]:


# create a list of years 
years = list(map(str, range(1980,2014)))
print(years)


# In order to create a `Choropleth` map, we need a GeoJSON file that defines the areas/boundaries of the state, county, or country that we are interested in. In our case, since we are endeavoring to create a world map, we want a GeoJSON that defines the boundaries of all world countries. For your convenience, we will be providing you with this file, so let's go ahead and load it.
# 

# In[6]:


pip install geojson


# In[7]:


# import gesojson map file
import geojson


# In[32]:


import requests
json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json'
resp = requests.get(json_url)
world_geo=resp.text
world_geo


# In[13]:


# create a plain world map
world_map = fo.Map(location=[0, 0], zoom_start=2)


# And now to create a `Choropleth` map, we will use the *choropleth* method with the following main parameters:
# 
# 1.  `geo_data`, which is the GeoJSON file.
# 2.  `data`, which is the dataframe containing the data.
# 3.  `columns`, which represents the columns in the dataframe that will be used to create the `Choropleth` map.
# 4.  `key_on`, which is the key or variable in the GeoJSON file that contains the name of the variable of interest. To determine that, you will need to open the GeoJSON file using any text editor and note the name of the key or variable that contains the name of the countries, since the countries are our variable of interest. In this case, **name** is the key in the GeoJSON file that contains the name of the countries. Note that this key is case_sensitive, so you need to pass exactly as it exists in the GeoJSON file.

# In[22]:


# generate choropleth map using the total immigration of each country to Canada from 1980 to 2013
world_map.choropleth(
    geo_data=world_geo,
    data=df,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Immigration to Canada'
)

# display map
world_map


# ![image.png](attachment:image.png)

# *-> As per our `Choropleth` map legend, the darker the color of a country and the closer the color to red, the higher the number of immigrants from that country. Accordingly, the highest immigration over the course of 33 years (from 1980 to 2013) was from China, India, and the Philippines, followed by Poland, Pakistan, and interestingly, the US.*

# Notice how the legend is displaying a negative boundary or threshold. Let's fix that by defining our own thresholds and starting with 0 instead of -6,918!

# In[23]:


# create a numpy array of length 6 and has linear spacing from the minimum total immigration to the maximum total immigration
threshold_scale = np.linspace(df['Total'].min(),
                              df['Total'].max(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist() # change the numpy array to a list
threshold_scale[-1] = threshold_scale[-1] + 1 # make sure that the last value of the list is greater than the maximum immigration

# let Folium determine the scale.
world_map = fo.Map(location=[0, 0], zoom_start=2)
world_map.choropleth(
    geo_data=world_geo,
    data=df,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    threshold_scale=threshold_scale,
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Immigration to Canada',
    reset=True
)
world_map


# ![image.png](attachment:image.png)

# In[26]:


df['Total'].astype({"Total":int})
df_tot = df[['Country','Total']]


# In[27]:


df_tot.dtypes


# In[28]:


df_tot.head()


# ## Plot Choropleth map

# In[44]:


world_map = fo.Map(location=[0, 0], zoom_start=2)

fo.Choropleth(geo_data = world_geo, name = "choropleth", data = df_tot, 
            columns = ["Country","Total"], 
            key_on = 'feature.properties.name',
            fill_color = "YlOrRd",
            fill_opacity = 0.7, 
            line_opacity = 0.5,
            legend_name = "Number of Immigrants to Canada",
            legend_color = 'White'
            ). add_to(world_map)

style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}

highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

color_scale = fo.features.GeoJson(
      world_geo,
      style_function=style_function, 
      control=False,
      highlight_function=highlight_function,
    # add tooltip 
      tooltip = fo.features.GeoJsonTooltip(
      fields = ["name"], 
      aliases = ["Country:"],
      style =("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;" ))
      )

world_map.add_child(color_scale)
world_map.keep_in_front(color_scale)
# add layer control 
fo.LayerControl().add_to(world_map)
world_map


# ![image-2.png](attachment:image-2.png)

# In[ ]:




