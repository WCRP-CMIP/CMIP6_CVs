To register (or edit) information about your model, please title your issue "source_id registration of [acronym for your model]" and  provide the following information:

'label' -- A short acronym that uniquely identifies your model (and distinguishes it from other versions of your model used in CMIP6).

'label_extended' -- An extended identifier for more verbose model identifying information

'source_id' -- An identifier that should be identical to "label" but with forbidden characters either removed or replaced by a hyphen ("-").  The source_id will appear in the ESGF search interface and in filenames a subdirectory names. Restrict characters used in source_id to the following set:  a-z, A-Z, 0-9, and "-".

'institution_id' -- list all institutions (by institution_id) who are responsible for one or more CMIP6 simulations with this model version. Additional institutions can be added to the list as needed, but only institutions registered (see above) may be included.

'release_year' -- this should be the year your model was first used in a scientific study. This year should reflect the "generation" of models rather than distinguishing between closely-related versions.

'activity_participation' -- The CMIP6 MIPs that you intend to run experiment simulations (See https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_activity_id.json)

Next you should provide further information about any named component models comprising your coupled model. If a component is missing from your model, indicate this with "None". If a component is included but unnamed in your model (i.e., without an identifying name), indicate this with "unnamed". For a "named" component model specify first the name (presumably an acronym) then provide whatever additional information you think is appropriate, identifying the version and perhaps resolution of the component model (see examples below). Here are the components that should be defined (and if necessary and appropriate, you may add others):

"aerosol", "atmos", "atmosChem", "land", "landIce", "ocean", "ocnBgchem", and "seaIce". Full descriptors of these fields can be found in the CMIP6_realm.json file (see https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_realm.json). Accepted entries for "nominal_resolution" can be found in the CMIP6_nominal_resolution.json file (see https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_nominal_resolution.json)

Example:
[title your issue: "source_id registration of ACCESS-1-0"]

    label = ACCESS 1.0
    label_extended = ACCESS 1.0 (This entry is free text for users to contribute verbose information)
    source_id = ACCESS-1-0 (an alternative could be "ACCESS1-0")
    institution_id = CSIRO-BOM
    release_year = 2011
    activity_participation = [CMIP]

    aerosol:
    description = CLASSIC (v1.0)
    nominal_resolution = 100 km
    atmos:
    description = HadGAM2 (r1.1, N96; 192 x 145 longitude/latitude; 38 levels; top level 39255 m)
    nominal_resolution = 100 km
    atmosChem:
    description = none
    nominal_resolution = none
    land:
    description = MOSES2.2
    nominal_resolution = 100 km    
    landIce:
    description = none
    nominal_resolution = none 
    ocean:
    description = ACCESS-OM (MOM4p1, tripolar primarily 1deg; 360 x 300 longitude/latitude; 50 levels; top grid cell 0-10 m)
    nominal_resolution = 100 km
    ocnBgchem:
    description = none
    nominal_resolution = none
    seaIce:
    description = CICE4.1
    nominal_resolution = 100 km
