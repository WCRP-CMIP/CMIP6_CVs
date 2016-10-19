<Here you may register your institution, register your model, or raise other issues concerning CMIP6 controlled vocabularies.  Please follow the appropriate template below, and then delete any irrelevant text before submitting.>

*********************************************
## Registering your institution
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

*********************************************
## Registering your model
*********************************************
To register (or edit) information about your model, please title your issue "source_id registration of [acronym for your model]" and  provide the following information:

'label' -- A short acronym that uniquely identifies your model (and distinguishes it from other versions of your model used in CMIP6). This label is limited to 16 characters in length.

'source_id' -- An identifier that should be identical to "label" but with forbidden characters either removed or replaced by a hyphen ("-").  The source_id will appear in the ESGF search interface and in filenames a subdirectory names.  Restrict characters used in source_id to the following set:  a-z, A-Z, 0-9, and "-".

'institution_id' -- list all institutions (by institution_id) who are responsible for one or more CMIP6 simulations with this model version.  Additional institutions can be added to the list as needed, but only institutions registered (see above) may be included.

'release_year' -- this should be the year your model was first used in a scientific study.  This year should reflect the "generation" of models rather than distinguishing between closely-related versions.

Although the additional information is not required, we encourage you to also provide the identifying descriptions of the component models comprising your coupled model.  If a component is missing from your model, indicate this with "None".  If a component is included but unnamed in your model (i.e., without an identifying name), indicate this with "unnamed".  For a "named" component model specify first the name (presumably an acronym) then provide whatever additional information you think is appropriate, identifying the version and perhaps resolution of the component model (see examples below).  Here are the components that should be defined (and if necessary and appropriate, you may add others):

"aerosol", "atmosphere", "atmospheric_chemistry", "land_ice", "land_surface", "ocean", "ocean_biogeochemistry", and "sea_ice".

Example:
[title your issue: "source_id registration of ACCESS-1-0"]

    label = ACCESS 1.0 (limited to 16 characters)
    source_id = ACCESS-1-0 (an alternative could be "ACCESS1-0")
    institution_id = CSIRO-BOM
    release_year = 2010

    label_extended = ACCESS 1.0 (r105557) [You can use this identifier to extend upon the limited 16 characters for "label" to describe your model]
    aerosol = unnamed
    atmosphere = HadGAM2 (r1.1; 192 x 145 N96; 38 levels; top level 39255m)
    atmospheric_chemistry = None
    land_ice = None
    land_surface = MOSES2.2
    ocean = ACCESS-OM (MOM4p1; tripolar primarily 1 deg latitude/longitude; 50 levels; top grid cell 0-10m),
    ocean_biogeochemistry = None
    sea_ice = CICE4.1 
    
The first 4 entries above are required; the additional entries are "free text".  Please provide as much information as you think would be useful in identifying your model, but avoid details you are not certain are correct.

*********************************************
## Raising other issues
*********************************************
Your issue "title" should begin with the name of the Controlled Vocabulary of interest and also include a terse indication of the issue (e.g., "activity_id -- add 'PMIP'"). 
