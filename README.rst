Project Summary
===============

As you can see this project is a fork of openscriptures/openscriptures. This is an area for experimentation and prototyping. 
Because of the nature of opensource, decisions for feature inclusion often take time, whereas in a separate project fast prototyping can be accomplished, and merged back in once decisions are made.

This project is a django project, and django is currently its only dependency. The project is divided into several logical applications described below.

Django apps
------------

- Core
	This is a data app. All the database models for storing scriptural and related data are in this app. This app will also contain a RESTful API that other apps can interface with.
- Frontends
	These apps contain the mostly client side code and show examples of how the API can be used to create a killer web 2.0 application. This validates the usefulness of the API, shows a proof of concept and has potential to become a very useful Bible tool.

	- Frontend ajax
		This app is built on jquery, and is progressing nicely, although work has been paused for work on the sproutcore frontend. The design is not final, but has some good layout concepts in it.
	
	- Frontend sproutcore
		Just starting this frontend built on sproutcore. Sproutcore was chosen because it is the best html5 javascript application platform to date. Same basic idea as the jquery frontend but with great potential to feel like a desktop app!

Upcoming apps
~~~~~~~~~~~~~

The following three apps are placeholders for what is to come. While they will likely share the same frontends (ajax & sproutcore) the server-side logic needs to have its own app for sake of organization and readability.

- Study
	This will replace the Bible reader prototype and will be expanded to add as many study tools as we are able such as tags, highlights, notes, periccopes, etc.
- Compare
	This will replace the manuscript comparator. Again, it will use the same frontend for display, but the API calls will need to be different and have special logic for this app.
- Semantic Linker
	This app is where translated texts are linked with the unified manuscript to create semantically linked data.