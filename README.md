# Example
![frame100](https://github.com/andjnewb/DaD_Analytics/assets/71988305/aa433bb1-6f8e-4449-91d5-74e20b03cd23)
![Capture](https://github.com/andjnewb/DaD_Analytics/assets/71988305/c544d727-bd97-480a-a5c3-de0fd9cea7e9)
![Capture](https://github.com/andjnewb/DaD_Analytics/assets/71988305/0d0bfe3e-89df-4570-aaae-8a97c5d0c21e)

Double counting is currently a problem, and I'm exploring ways around it.  

The current data can be viewed here. As this project is under development, the data is only sporadically updated and not at all accurate. Once I have confidence in its function, I plan to set up a machine to continously analyze the market.  

(Dark and Darker Weapon Volume Example) https://charts.mongodb.com/charts-project-0-xvjic/public/dashboards/659f7e6c-6593-4a81-819c-b70b648851ee  

# Status  
The project has had some major changes here recently. Firstly, I've moved the project from MongoDB to PostgreSQL, currently hosted on Cockroach Labs. It wasn't my first choice, but Cockroach Labs had the best free tier I could find so it went from MongoDB to MySQL to PostgreSQL in the span of a few days. The frontend is still up in the air, as most of the "free services" for this sort of things are actually not free but just trying to hook you in. 

On the python side, the main scripts can now analyze a given image and determine both volume and average price. I'm still having issues getting Docker to work on my machine(therefore I can't infer on images locally), and until I sort that out the project won't be running continously. Any data you see is just from sample runs. 


# Planned features
At a minimum, I would like to be able to analyze both volume and average prices. One of the issues is that sellers may describe their pricing with any arbitrary string of text. An auction house system is on the way from Ironmace that will hopefully make this easier. I'm not sure if rarity will ever be able to be analyzed, as the game uses a color system for rarity and Tesseract doesn't support color. Whenever the auction house drops, I'll have to redo the Roboflow model. That's part of the fun for developing tools for an in-progress game I suppose.



# Technology and tools used
Python  

Roboflow (https://universe.roboflow.com/dadproject/detect-chat-dad)  

Tesseract OCR  

PostgreSQL(Hosted on Cockroach Labs).
