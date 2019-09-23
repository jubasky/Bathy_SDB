# Bathy_SDB
Python application for Bathymetric data management with PostGis.
I aimed to create a practical and functional solution for storing and accessing 
high resolution bathymetric and topographic data in an efficient way, using free software (FOSS). 
A PostgreSql (version 9.3) relational database system was used,
complemented by PostGis extensions for spatial data, 
and the “pgpointcloud” library extension for pointcloud data structures. 
Each bathymetric record, stored as sets (Pcpatches) of Pointcloud data structures,
has an associated metadata record describing the campaign/cruise,
QC, and other attributes.
This application was developed in the context of a GIS Master degree
in the University of Algarve, leveraging the differents skills 
acquired during the course to produce a useful tool for a 
very specific data management need related with my work at IPMA.
The application has a simple set of functionalities. It allows the creation
of a new database and the ingestion of text files with bathymetric information 
namely x and y coordinates, depth and acoustic backscatter and RGB values 
when available. Functions such as data visualization, edition, export
of custom xml formatted metadata, were also developed.
The application was designed as a simple tool for a defined purpose (bathymetric 
data requests) and to experiment and test pointcloud data structures.  
It was developed with Pithon 2.7 using Qt 4.8 / PyQt4 libraries and Qgis 2.10.1 API. 
