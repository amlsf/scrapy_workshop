Scrapy Workshop
===============

Data Collection with Scrapy: Build &amp; Manage Production Web Scraping Pipelines


Install instructions here...


Website to be crawling here... what we are crawling for


Presentation link here... 


Additional resources to get familiar with here... 



LocalVector Maps
=================
LocalVector Maps is an interactive real estate data visualization tool that uses colorful choropleth maps and graphs as an intuitive approach to help residential real estate buyers quickly absorb a large amount of data in order to compare trends, identify specific high growth areas, visualize market recovery since the most recent meltdown, and explore homes currently for sale within five Bay Area counties. My goal was to build a unique real estate research tool that was intuitive and easy to gain a high level, comparative overview of the landscape but also offer enough granularity to be able to drill in and identify specific opportunities.

The application uses over 200,000 rows of licensed Multiple Listing Services real estate data as well as geospatial data from the US Census Bureau. This project will be incorporated as a new feature in the website of LocalVector, a Bay Area real estate search engine.

I built this application because I noticed a lack exploratory tools for non-professional investors like the mom-and-pops, particularly tools that presented data with maps focused on change over time in addition to price level snapshots. While line graphs are popularly used and also certainly show growth, they are limiting in granularity and the number of regions that can be compared in a single visualization.

Developed in 3.5 weeks at Hackbright Academy's Software Engineering Fellowship in the Spring 2014 cohort. 

#####Note on cloning this repository:
Note that this application uses licensed Multiple Listing Services (MLS) data, it is not possible to run this repository locally on your machine. The link will be posted once the app is successfully integrated into Local Vector. 

#####Technology used:
This application is built using the Flask framework and is written in Python in the back-end, Javascript in the front-end, and uses a PostgreSQL database.

1. Front-end: Javascript, jQuery, AJAX, HTML, CSS, Bootstrap, D3
2. Back-end: Python, Flask, SQLAlchemy, PostgreSQL, numpy module
3. GIS-related: Leaflet API, Mapbox, QuantumGIS, GeoJSON, Python shapefile library, markercluster library

Summary of Features
-------------------

![Main page](/screenshots/2salespricepage.JPG)
![yoy page](/screenshots/1YoYpricechange.JPG)

#####1. Choropleth Map 
The map offers visualization of 3 different metrics split out by zipcode. A button in the control panel on the left toggles off the choropleth layer if users need a clearer view of the map. For a more intuitive experience, the controls showing the metric options disappear when the user toggles off the choropleth. The three metric options displayed on the map are:  
  *	Median sales price of homes by zipcode
  *	Median sales price per square foot by zipcode
  *	Percent change in median sales price between any two years of the user's choice 
      *	This uses a diverging color scheme instead of a sequential one as in the metrics above. 
      *	The Python script ensures a minimum number of houses in each region for a more accurate representation of the data.

#####2. Range slider for year on year comparison
  * When a user selects the third metric (price change comparison) to view, a range slider appears that allows a selection of any base year and comparison year to view the % change in median price between the two years across all regions. 

#####3.	Information boxes on mouseover
  * When the mouse hovers over any region, the region is highlighted and an information box on the upper right corner appears to drill down into additional details about the region such as median price and number of homes sold, and exact % change where appropriate.
  * The Price Comparison option view shows in the mouseover information box a time series graph displaying the median price/sqft each year for the respective region.
  * Clicking on any particular region automatically zooms in to pull the region into the full viewport.

#####4.	Legend 
  *	The legend updates dynamically with the dataset with a clear label that updates based on the metric and years selected giving the user a clear understanding of what is displayed.
  *	The code allows the legend to automatically scale with the range of any particular dataset that the user chooses to view.

#####5.	Toggle to view homes currently for sale
  *	In the control panel on the left, a button allows the user to toggle on markers for active listings. When the users click on the markers, a pop-up displays showing detailed listing information including list price, address, # of beds/bath, a description of the property, and the MLS listing number. Users can click on the address and be taken to a separate detailed listings page  
  *	The display uses a markercluster library to avoid overwhelming the user with too many markers and improve performance. When the user mouses over a particular cluster, a polygon appears on the map indicating what area of the map the cluster covers. Clicking on the cluster automatically zooms into the map and splits clusters out into smaller clusters or map pins. Double clicking zooms back out to the original view.   
![Other page](/screenshots/1-activelistings.JPG)
![Local page](/screenshots/11-activelistings2.JPG)

Project Walk Through
--------------------
###Planning
######Leafletjs, Mapbox tile server, OpenStreetMap

