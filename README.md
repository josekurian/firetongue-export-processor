# firetongue-export-processor
This project has several goals ...
* Provide the means to browse and search the data of my music data catalogue which has been done with FireTongue OrangeCD http://www.firetongue.com/
* Creating a simple project that my son can develop his Python skills. So as his skills progress he can build out the solution. As a result there are some releases to use a simple start milestones

## How it works

The OrangeCD tool creates an XML export. This is then read when the application starts up. Then through the browser it can extract data and return the relevant information rendering it as HTML.

To do this, it uses Python3 with:
* Flask web server (https://flask.palletsprojects.com/en/2.1.x/)
* Jinja for rendering the results (https://jinja.palletsprojects.com/en/3.1.x/)
* ElementTree (https://docs.python.org/3/library/xml.etree.elementtree.html) for working with the export file

The server needs to be started up with the path to the OrangeCD Exported file. The code is layed out to separate the logic examining the XML compared the web functionality.
* main.py - the Flask handling logic.
* data.py - the Logic for locating and retrieving data from the export file
* constants.py - defined strings for the different attributes and elements in the export file
* svr_config.py - provides the values needed for the Flask server such as the host and port numbers, whether the enable debug etc.
* /templates - folder for the Jinja templates

