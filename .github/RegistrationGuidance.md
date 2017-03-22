You must register your institution and model before you can "publish" your CMIP6 output on ESGF.  This should be done by submitting two issues on the [CMIP6_CVs issue page](https://github.com/WCRP-CMIP/CMIP6_CVs/issues/new?title=CV), one for your institution and one for your model.  Here we specify what information you should provide:

*********************************************
## Register your institution
*********************************************
To register (or edit) information about your institution, please title your issue "institution_id registration of [acronym for your institution]" and  provide the following information:

'institution_id'  -- a short acronym suitable for search interfaces and sub-directory names (should limit the characters used to the following set: a-z, A-Z, 0-9, and "-")
'institution' -- full name and address of institution, likely to include: laboratory/group name, hosting institution name, city, state/province and postal-code, country  (no restriction on character set).

Example 1:
[title your issue "institution_id registration of PCMDI"]

    institution_id = PCMDI
    institution = Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA
    
Example 2:
[title your issue "institution_id registration of NASA-GISS"]

    institution_id = NASA-GISS
    institution = NASA Goddard Institute for Space Studies, New York, NY 10025, USA 
    
If you suspect your institution may have already been registered, first check [CMIP6_institution_id.html](http://rawgit.com/WCRP-CMIP/CMIP6_CVs/master/src/CMIP6_institution_id.html); there is no reason to register it again.

*********************************************
## Register your model
*********************************************
To register (or edit) information about your model, please title your issue "source_id registration of [acronym for your model]" and  provide the following information:

'label' -- A short acronym that uniquely identifies your model (and distinguishes it from other versions of your model used in CMIP6). This label is limited to 16 characters in length.

'source_id' -- An identifier that should be identical to "label" but with forbidden characters either removed or replaced by a hyphen ("-").  The source_id will appear in the ESGF search interface and in file names and directory trees.  Restrict characters used in source_id to the following set:  a-z, A-Z, 0-9, and "-".

'institution_id' -- list all institutions (using their "institution_id" acronyms) responsible for running CMIP6 simulations with this model version.  Additional institutions can be added to the list as needed, but only institutions registered (see above) may be included.

'release_year' -- this should be the year your model was first used in a scientific study.  This year should reflect the "generation" of models rather than distinguishing between closely-related versions.

'activity_participation' -- A comma-separted list of the MIPs to which you intend to contribute.  Include those that are currently in your plans; you can add additional MIPs later.  Please select from the official activity_id's recorded in the [activity_id CV](https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_activity_id.json).  Note that if you plan to run the "DECK" simulations, indicate this by including "CMIP" in your list.

'nominal_resolution' -- For the atmosphere, ocean, and land_ice models, please also record the nominal_resolution.  The definition and algorithm for calculating nominal resolution can be found in Appendix 2 of the [CMIP6 Global Attributes, DRS, Filenames, Directory Structure, and CV’s document](https://docs.google.com/document/d/1h0r8RZr_f3-8egBMMh7aqLwy3snpD6_MrDz1q8n5XUk/edit).

Although not required initially, we strongly encourage you to also provide the identifying descriptions of the component models comprising your coupled model, including grid information.  If a component is missing from your model, indicate this with "None".  If a component is included but unnamed in your model (i.e., without an identifying name), indicate this with "unnamed".  For a "named" component model specify first the name (presumably an acronym) then provide whatever additional information you think is appropriate, identifying the version and perhaps resolution of the component model (see examples below).  

Here are the components that should be defined (and if necessary and appropriate, you may add others):
"aerosol", "atmosphere", "atmospheric_chemistry", "land_ice", "land_surface", "ocean", "ocean_biogeochemistry", and "sea_ice".

Example:
[title your issue: "source_id registration of ACCESS-1-0"]

    activity_participation = CMIP, PMIP, CFMIP
    aerosol = CLASSIC (v1.0)
    atmosphere = HadGAM2 (r1.1; N96, 192 x 145 longitude/latitude; 38 levels; top level 39255 m)    
    atmospheric_chemistry = None
    institution_id = CSIRO-BOM
    label = ACCESS 1.0    ![limited to 16 characters]
    label_extended = ACCESS 1.0 (r105557) ![Use this identifier to extend the 16 character limit for "label" to describe your model]
    land_ice = None
    land_surface = MOSES2.2
    nominal_resolution_atmos = 100 km
    nominal_resolution_landIce = None   ![unless your climate model includes a dynamic ice sheet model.]
    nominal_resolution_ocean = 100 km
    ocean = ACCESS-OM (MOM4p1; tripolar primarily 1deg, 360 x 300 longitude/latitude; 50 levels; top grid cell 0-10 m)    
    ocean_biogeochemistry = None
    release_year = 2011
    sea_ice = CICE4.1
    source_id = ACCESS-1-0 (limited to 16 characters)
    
The entries institution_id, label, label_extended, source_id, activity_participation, and nominal_resolution (of atmosphere, ocean and land ice) are all required and must strictly adhere to the guidance above; the additional entries should follow the above example.
