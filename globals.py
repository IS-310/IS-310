#! usr/bin/env python3

import shelve

sh = shelve.open('globals')
sh['blindStatus'] = 0
sh.close()