The IM_Climate Toolkit is a utility package for finding climate stations and downloading climate parameter data for a station or stations.  

#### Overview ####

To serve the broadest user community, it is implemented in both Python and R. Regardless of language, it provides data access via ACIS web services (http://www.rcc-acis.org/docs_webservices.html) to station information and station data that:

+ Supports basic data request functions using consistent (identical) logic:

  * findStation
  * requestData

+ Formats outputs consistently regardless of implementation technique (R, Python)

  * Limits alteration to data returned from ACIS web services


#### Python - Installing the IM_Climate Package ####

The package can be installed from this GitHub repository by first installing and loading the [devtools](https://github.com/hadley/devtools) library from CRAN. Then, run the

```
install_github("IMDProjects/IM_Climate/IM_Climate_py")
```
operation to grab the package code and install it locally. 
