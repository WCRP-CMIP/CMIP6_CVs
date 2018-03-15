#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:25:33 2018

This file cleans up the existing repo tags following discussions contained in
https://github.com/WCRP-CMIP/CMIP6_CVs/issues/448

PJD 31 Jan 2018     - Started

https://stackoverflow.com/questions/21738647/change-date-of-git-tag-or-github-release-based-on-it

# This moves you to the point in history where the commit exists
git checkout SHA1_OF_PAST_COMMIT

# This command gives you the datetime of the commit you're standing on
git show --format=%aD  | head -1

# And this temporarily sets git tag's clock back to the date you copy/pasted in from above
GIT_COMMITTER_DATE="Thu Nov 11 12:21:57 2010 -0800" git tag -a 0.9.33 -m"Retroactively tagging version 0.9.33"

# Combining the two...
GIT_COMMITTER_DATE="$(git show --format=%aD  | head -1)" git tag -a 0.9.33 -m"Retroactively tagging version 0.9.33"

Instead, you must remove the tag locally:
git tag -d 1.0.1

Push that deletion remotely:
git push origin :refs/tags/1.0.1

On GitHub, reload Releases—the release has now been marked as a "Draft"—and remove the draft.

Now, add the backdated tag based on the instructions above, and finally push the resulting tag to GitHub:
git push --tags


180222 Notes for MacOS 10.12.6

On mac XCode command line tools are required (otherwise a "missing xcrun" error occurs)
see https://apple.stackexchange.com/questions/254380/macos-sierra-invalid-active-developer-path

@author: durack1
"""
import os,subprocess
os.chdir('/sync/git/CMIP6_CVs')

#%% Create cleanup list
# [durack1ml:sync/git/CMIP6_CVs] durack1% git show-ref --tags
tagClean = []
tagClean.append('3.2.0')
tagClean.append('3.2.1')
tagClean.append('3.2.2')
tagClean.append('3.2.3')
tagClean.append('3.2.4')
tagClean.append('3.2.5')
tagClean.append('3.2.6')
tagClean.append('3.2.7')
tagClean.append('3.2.8')
#tagClean.append('3.3.0')
#tagClean.append('CMOR-3.2.5')
tagClean.append('CMOR-3.2.7')
tagClean.append('CMOR-3.2.8')
#tagClean.append('CMOR-3.3.0')

#%% Iterate over list to delete existing tags
for count,tag in enumerate(tagClean):
    print 'tag:    ',tag
    # Git delete existing tag
    subprocess.call(['git','tag','-d',tag])
    # And push to remote
    subprocess.call(['git','push','origin',''.join([':refs/tags/',tag])])

#%% Create target dictionary
tagList = {}
'''
tagList['6.2.0.1'] = {}
tagList['6.2.0.1']['Comment'] = '3.2.0/CMOR-3.2.0'
tagList['6.2.0.1']['MD5'] = '5c4bbac517cb2053c6d43957d552cd435809055a'
tagList['6.2.0.2'] = {}
tagList['6.2.0.2']['Comment'] = '3.2.1/CMOR-3.2.1'
tagList['6.2.0.2']['MD5'] = 'f5b0ef598a110f60a474f1f271b54ee2b417ee0d'
tagList['6.2.0.3'] = {}
tagList['6.2.0.3']['Comment'] = '3.2.2/CMOR-3.2.2'
tagList['6.2.0.3']['MD5'] = '511ab24b89bedbb242e0783a7815670ceab349bd'
tagList['6.2.0.4'] = {}
tagList['6.2.0.4']['Comment'] = '3.2.3/CMOR-3.2.3'
tagList['6.2.0.4']['MD5'] = '41fd650dd7b79b74783dd587b3103582d7934a82'
tagList['6.2.0.5'] = {}
tagList['6.2.0.5']['Comment'] = '3.2.4/CMOR-3.2.4'
tagList['6.2.0.5']['MD5'] = 'b48ad53b379141b22ed833fa39d9902b5c2ffe2e'
tagList['6.2.0.6'] = {}
tagList['6.2.0.6']['Comment'] = '3.2.5/CMOR-3.2.5'
tagList['6.2.0.6']['MD5'] = '8537f933f1b658f9e23251710a1bfd820c8f2594'
tagList['6.2.0.7'] = {}
tagList['6.2.0.7']['Comment'] = '3.2.6/CMOR-3.2.6'
tagList['6.2.0.7']['MD5'] = 'a4f9cf0dfb3be62a2d0daf09b3e9e3512a887196'
tagList['6.2.0.8'] = {}
tagList['6.2.0.8']['Comment'] = '3.2.7/CMOR-3.2.7'
tagList['6.2.0.8']['MD5'] = 'df18ec966ba2c5dfa2d446010395a40a1ac05d7e'
tagList['6.2.0.9'] = {}
tagList['6.2.0.9']['Comment'] = '3.2.8/CMOR-3.2.8'
tagList['6.2.0.9']['MD5'] = '3bbbc883bfaf7a8f99cd50603bbf3199491d7c49'
tagList['6.2.0.10'] = {}
tagList['6.2.0.10']['Comment'] = '3.3.0/CMOR-3.3.0'
tagList['6.2.0.10']['MD5'] = 'bb42f99cd16b72929fad46d068de922cadcb4db2'
tagList['6.2.0.11'] = {}
tagList['6.2.0.11']['Comment'] = '3.3.1/CMOR-3.3.1'
tagList['6.2.0.11']['MD5'] = 'ac4b169b03595f65b6f21ebe86f0aa7e7f55e45b'
#tagList['6.2.1.0'] = {}
#tagList['6.2.1.0']['Comment'] = '6.2.1.0'
#tagList['6.2.1.0']['MD5'] = ''
# 180315 1205
tagList['6.2.3.3'] = {}
tagList['6.2.3.3']['Comment'] = 'Updated to include ARTS-2-3; Awaiting cohort guidance (#453)'
tagList['6.2.3.3']['MD5'] = '07044624a04316c533a87819664044f738715269'
tagList['6.2.3.4'] = {}
tagList['6.2.3.4']['Comment'] = 'Register source_id LBLRTM (#484)'
tagList['6.2.3.4']['MD5'] = '6d8065c5d35785e58160e8f1b7789a7998ca0f6f'
tagList['6.2.3.5'] = {}
tagList['6.2.3.5']['Comment'] = 'Revise source_id GFDL-ESM4 to include CDRMIP (#485)'
tagList['6.2.3.5']['MD5'] = 'e99a005ce580cfd6f3e66d1fcd43abab36ffd9e5'
'''

#%% Iterate over dictionary to create new tags and delete existing
# Should look like
# git tag -l | while read -r tag; do `git checkout $tag && git tag -d $tag &&\
# git push origin :refs/tags/$tag &&\
# GIT_COMMITTER_DATE="$(git show --format=%aD | head -1)" git tag -a $tag\
# -m"$tag"`; done; git push --tags
'''
for tag in tagList.keys():
    print 'tag:    ',tag
    print 'comment:',tagList[tag]['Comment']
    print 'MD5:    ',tagList[tag]['MD5']
    # Git checkout tag hash
    subprocess.call(['git','checkout',tagList[tag]['MD5']])
    # Get timestamp of hash
    cmd = 'git show --format=%aD|head -1'
    ps = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    timestamp = ps.communicate()[0].rstrip()
    print timestamp
    # Generate composite command and execute
    cmd = ''.join(['GIT_COMMITTER_DATE="',timestamp,'" git ','tag ','-a ',tag,
                   ' -m"',tagList[tag]['Comment'],'"'])
    print cmd
    subprocess.call(cmd,shell=True) ; # Shell=True required for string
# And push all new tags to remote
subprocess.call(['git','push','--tags'])
'''
#%% Logs
''' 180222 1536
[durack1ml:git/CMIP6_CVs/src] durack1% python cleanupTags.py
tag:     3.2.0
Deleted tag '3.2.0' (was 5c4bbac)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.0
tag:     3.2.1
Deleted tag '3.2.1' (was f5b0ef5)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.1
tag:     3.2.2
Deleted tag '3.2.2' (was 511ab24)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.2
tag:     3.2.3
Deleted tag '3.2.3' (was 41fd650)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.3
tag:     3.2.4
Deleted tag '3.2.4' (was b48ad53)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.4
tag:     3.2.5
Deleted tag '3.2.5' (was 8537f93)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.5
tag:     3.2.6
Deleted tag '3.2.6' (was a4f9cf0)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.6
tag:     3.2.7
Deleted tag '3.2.7' (was df18ec9)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.7
tag:     3.2.8
Deleted tag '3.2.8' (was 3bbbc88)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.2.8
tag:     3.3.0
Deleted tag '3.3.0' (was bb42f99)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         3.3.0
tag:     CMOR-3.2.5
Deleted tag 'CMOR-3.2.5' (was 8537f93)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         CMOR-3.2.5
tag:     CMOR-3.2.7
Deleted tag 'CMOR-3.2.7' (was 0a87d44)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         CMOR-3.2.7
tag:     CMOR-3.2.8
Deleted tag 'CMOR-3.2.8' (was 3bbbc88)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         CMOR-3.2.8
tag:     CMOR-3.3.0
Deleted tag 'CMOR-3.3.0' (was bb42f99)
To git@github.com:WCRP-CMIP/CMIP6_CVs
 - [deleted]         CMOR-3.3.0
tag:     6.2.0.1
comment: 3.2.0/CMOR-3.2.0
MD5:     5c4bbac517cb2053c6d43957d552cd435809055a
HEAD is now at 5c4bbac... Issue115 durack1 register institution id cnrm cerfacs (#154)
Mon, 21 Nov 2016 15:34:45 -0800
Traceback (most recent call last):
  File "cleanupTags.py", line 131, in <module>
    subprocess.call(cmd)
  File "/Volumes/durack1ml/Users/durack1/anaconda2/lib/python2.7/subprocess.py", line 168, in call
    return Popen(*popenargs, **kwargs).wait()
  File "/Volumes/durack1ml/Users/durack1/anaconda2/lib/python2.7/subprocess.py", line 390, in __init__
    errread, errwrite)
  File "/Volumes/durack1ml/Users/durack1/anaconda2/lib/python2.7/subprocess.py", line 1025, in _execute_child
    raise child_exception
OSError: [Errno 2] No such file or directory
180315 1205

(uvcdat2120) trustym:src paul$ python cleanupTags.py 
tag:     6.2.3.4
comment: Register source_id LBLRTM (#484)
MD5:     6d8065c5d35785e58160e8f1b7789a7998ca0f6f
M	src/cleanupTags.py
Note: checking out '6d8065c5d35785e58160e8f1b7789a7998ca0f6f'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

HEAD is now at 6d8065c... Register source_id LBLRTM (#484)
Mon, 12 Mar 2018 18:54:13 -0700
GIT_COMMITTER_DATE="Mon, 12 Mar 2018 18:54:13 -0700" git tag -a 6.2.3.4 -m"Register source_id LBLRTM (#484)"
tag:     6.2.3.5
comment: Revise source_id GFDL-ESM4 to include CDRMIP (#485)
MD5:     e99a005ce580cfd6f3e66d1fcd43abab36ffd9e5
M	src/cleanupTags.py
Previous HEAD position was 6d8065c... Register source_id LBLRTM (#484)
HEAD is now at e99a005... Revise source_id GFDL-ESM4 to include CDRMIP (#485)
Mon, 12 Mar 2018 19:08:03 -0700
GIT_COMMITTER_DATE="Mon, 12 Mar 2018 19:08:03 -0700" git tag -a 6.2.3.5 -m"Revise source_id GFDL-ESM4 to include CDRMIP (#485)"
tag:     6.2.3.3
comment: Updated to include ARTS-2-3; Awaiting cohort guidance (#453)
MD5:     07044624a04316c533a87819664044f738715269
M	src/cleanupTags.py
Previous HEAD position was e99a005... Revise source_id GFDL-ESM4 to include CDRMIP (#485)
HEAD is now at 0704462... Updated to include ARTS-2-3; Awaiting cohort guidance (#453)
Mon, 12 Mar 2018 18:42:45 -0700
GIT_COMMITTER_DATE="Mon, 12 Mar 2018 18:42:45 -0700" git tag -a 6.2.3.3 -m"Updated to include ARTS-2-3; Awaiting cohort guidance (#453)"
Counting objects: 5, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (5/5), 726 bytes | 0 bytes/s, done.
Total 5 (delta 1), reused 2 (delta 1)
remote: Resolving deltas: 100% (1/1), done.
To github.com:WCRP-CMIP/CMIP6_CVs
 * [new tag]         3.2.0 -> 3.2.0
 * [new tag]         3.2.1 -> 3.2.1
 * [new tag]         3.2.2 -> 3.2.2
 * [new tag]         3.2.3 -> 3.2.3
 * [new tag]         3.2.4 -> 3.2.4
 * [new tag]         3.2.5 -> 3.2.5
 * [new tag]         3.2.6 -> 3.2.6
 * [new tag]         3.2.7 -> 3.2.7
 * [new tag]         3.2.8 -> 3.2.8
 * [new tag]         6.2.3.3 -> 6.2.3.3
 * [new tag]         6.2.3.4 -> 6.2.3.4
 * [new tag]         6.2.3.5 -> 6.2.3.5
 * [new tag]         CMOR-3.2.7 -> CMOR-3.2.7
 * [new tag]         CMOR-3.2.8 -> CMOR-3.2.8
'''