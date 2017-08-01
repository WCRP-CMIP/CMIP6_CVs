# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys, os, glob, cdms2

#  This script traps model names (acronyms) that were created by PCMDI for CMIP2.  These names likely can be improved. 
# PJG  05/31/17

pathin = '/work/cmip2/atm/mo/tas/'

lst = os.listdir(pathin)

print lst

##  REMOVE MULTI MODEL MEANS AND MEDIAN FROM LIST
new_lst = [ ]
shape_lst = [ ]
alias_size_dict ={ }
for l in lst:
   if l.find('median') == -1 and l.find('mean') == -1 and l.find('.tar')==-1:
      newer_lst = glob.glob(os.path.join(pathin,l,'*.nc',)) 
      f = cdms2.open(newer_lst[-1])
      d = f["tas"]
      x = d.shape
      axis = d.getAxisIds()
      shape_lst.append(x) 
      alias_size_dict[l] = {}
      alias_size_dict[l][axis[0]] = x[0]
      alias_size_dict[l][axis[1]] = x[1]
      alias_size_dict[l][axis[2]] = x[2]
      #alias_size_dict[l][axis[3]] = x[3]
      
#      print l
#      new_lst.append(l) 
print alias_size_dict
### PUT BAD NAMES IN DICTIONARY
#
#cmip2_change_mod_name = {}
#
#for n in new_lst:
#   cmip2_change_mod_name[n] = 'change me'
#
#print cmip2_change_mod_name.keys()
#
#print cmip2_change_mod_name
#
#
#print 'done'

