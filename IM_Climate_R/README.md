The IM_Climate Toolkit is a utility package for finding climate stations and downloading climate parameter data for a station or stations.  

#### Overview ####

To serve the broadest user community, it is implemented in both Python and R. Regardless of language, it provides data access via ACIS web services (http://www.rcc-acis.org/docs_webservices.html) to station information and station data that:

+ Supports basic data request functions using consistent (identical) logic:

  * findStation
  * requestData

+ Formats outputs consistently regardless of implementation technique (R, Python)

  * Limits alteration to data returned from ACIS web services

#### Release 1.6 - Spring 2017 ####

Functionality - Generic station discovery; station parameter summary; monthly data by year

#### Release 1.5 - 20170327 ####

Functionality - Get yearly gridded data (PRISM only)
  
#### Release 1.4 - Tabled - functionality moved to v1.6 ####

Functionality - Get yearly gridded data (PRISM only)

#### Release 1.3 - 20161215 ####

Functionality - Get monthly gridded data (PRISM only)
  
#### Release 1.2 - 20161122 ####

Functionality - Get monthly station summary by year for station data
  
#### Release 1.1 - 20161006 ####

Functionality - Get daily gridded data (PRISM only)
  
#### Release 1.0 - 20160906 ####


#### R - Installing the IM_Climate Package ####

The package can be installed from this GitHub repository by first installing and loading the [devtools](https://github.com/hadley/devtools) library from CRAN. __If you are on the NPS network__, run the

```R
library(httr)
set_config( config( ssl_verifypeer = 0L ) )
library(devtools)
install_github("IMDProjects/IM_Climate/IM_Climate_R")
```
operation to grab the package code and install it locally. 


Otherwise, run the

```R
library(devtools)
install_github("IMDProjects/IM_Climate/IM_Climate_R")
```
operation to grab the package code and install it locally.

#### Disclaimer ####
This software is in the public domain because it contains materials from the U.S. National Park Service, an agency of the United States Department of Interior.

Although this software package has been used by the U.S. National Park Service (NPS), no warranty, expressed or implied, is made by the NPS or the U.S. Government as to the accuracy and functioning of the package and related program material nor shall the fact of distribution constitute any such warranty, and no responsibility is assumed by the NPS in connection therewith.

This software is provided "AS IS."
