project = "Beej's Guide to Git"
copyright = 'Copyright © July 9, 2024'
author = 'Brian "Beej Jorgensen" Hall'
release = '0.0.5'

# Hacky Python to run the common conf file
import os
with open(os.sep.join((os.getenv('BGBSPS_DIR'), 'common-conf.py'))) as f: exec(f.read(), globals())
