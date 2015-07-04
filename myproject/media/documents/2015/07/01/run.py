#!/usr/bin/env python
import axmlparserpy.apk as apk
ap = apk.APK('1.apk')
print ap.get_package()
print ap.get_androidversion_name()