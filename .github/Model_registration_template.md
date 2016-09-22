To register (or edit) information about your model, please title your issue "source_id registration of <acronym for your model >" and  provide the following information:

'label' -- A short acronym that uniquely identifies your model (and distinguishes it from other versions of your model used in CMIP6).

'source_id' -- An identifier that should be identical to "label" but with forbidden characters either removed or replaced by a hyphen ("-").  The source_id will appear in the ESGF search interface and in filenames a subdirectory names.  Restrict characters used in source_id to the following set:  a-z, A-Z, 0-9, and "-".

'institution_id' -- list all institutions (by institution_id) who are responsible for one or more CMIP6 simulations with this model version.  Additional institutions can be added to the list as needed, but only institutions registered (see above) may be included.

'release_year' -- this should be the year your model was first used in a scientific study.  This year should reflect the "generation" of models rather than distinguishing between closely-related versions.

Next you should provide further information about any named component models comprising your coupled model.  If a component is missing from your model, indicate this with "None".  If a component is included but unnamed in your model (i.e., without an identifying name), indicate this with "unnamed".  For a "named" component model specify first the name (presumably an acronym) then provide whatever additional information you think is appropriate, identifying the version and perhaps resolution of the component model (see examples below).  Here are the components that should be defined (and if necessary and appropriate, you may add others):

"aerosol", "atmosphere", "atmospheric_chemistry", "land_ice", "land_surface", "ocean", "ocean_biogeochemistry", and "sea_ice".

Example:
[title your issue: "source_id registration of HadGAM2"]

    label = ACCESS 1.0
    source_id = ACCESS-1-0 (an alternative could be "ACCESS1-0")
    institution_id = UKMO
    release_year = 2010

    aerosol = unnamed
    atmosphere = HadGAM2 (r1.1; 192 x 145 N96; 38 levels; top level 39255m)
    atmospheric_chemistry = None
    land_ice = None
    land_surface = MOSES2.2
    ocean = ACCESS-OM (MOM4p1; tripolar primarily 1 deg latitude/longitude; 50 levels; top grid cell 0-10m)",
    ocean_biogeochemistry = None
    sea_ice = CICE4.1 
