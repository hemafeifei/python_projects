import shutil
import os
import re

# create a regex that match files with american date format.
date_pattern = re.compile(r"""^(.*?)
((0|1)\d)-
((0|1|2|3)\d)-
((19|20)\d\d)
(.*?)
""", re.VERBOSE)

# loop over the files in the working directory.
for f in os.listdir('.'):
    mo = date_pattern.search(f)

    if mo == None:
        continue

    before_part = mo.group(1)