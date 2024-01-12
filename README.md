# Example
![frame100](https://github.com/andjnewb/DaD_Analytics/assets/71988305/aa433bb1-6f8e-4449-91d5-74e20b03cd23)
![Capture](https://github.com/andjnewb/DaD_Analytics/assets/71988305/c544d727-bd97-480a-a5c3-de0fd9cea7e9)
![Capture](https://github.com/andjnewb/DaD_Analytics/assets/71988305/0d0bfe3e-89df-4570-aaae-8a97c5d0c21e)

Double counting is currently a problem, and I'm exploring ways around it.  

The current data can be viewed here. As this project is under development, the data is only sporadically updated and not at all accurate. Once I have confidence in its function, I plan to set up a machine to continously analyze the market.  

(Dark and Darker Weapon Volume Example) https://charts.mongodb.com/charts-project-0-xvjic/public/dashboards/659f7e6c-6593-4a81-819c-b70b648851ee  

# Planned features
At a minimum, I would like to be able to analyze both volume and average prices. One of the issues is that sellers may describe their pricing with any arbitrary string of text.  
The developers plan on implementing a Auction House style system, which makes me hesistant to put too much effort into the Roboflow model until that comes to fruition.  
For now, I am only working towards making volume accurate.


# Technology and tools used
Python  

Roboflow (https://universe.roboflow.com/dadproject/detect-chat-dad)  

Tesseract OCR  

MongoDB Cloud
