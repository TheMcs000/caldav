#!/usr/bin/env python

from unittest import TestCase
import vobject
import icalendar
import uuid
from caldav.lib.vcal import fix, create_ical
#from datetime import timezone
import pytz
from datetime import datetime, timedelta
from caldav.lib.python_utilities import to_normal_str, to_wire

#utc = timezone.utc
import pytz
utc = pytz.utc

# example from http://www.rfc-editor.org/rfc/rfc5545.txt
ev = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:19970901T130000Z-123403@example.com
DTSTAMP:19970901T130000Z
DTSTART;VALUE=DATE:19971102
SUMMARY:Our Blissful Anniversary
TRANSP:TRANSPARENT
CLASS:CONFIDENTIAL
CATEGORIES:ANNIVERSARY,PERSONAL,SPECIAL OCCASION
RRULE:FREQ=YEARLY
END:VEVENT
END:VCALENDAR"""


class TestVcal(TestCase):
    def assertSameICal(self, ical1, ical2):
        """helper method"""
        def normalize(s):
            s = to_wire(s).replace(b'\r\n',b'\n').strip().split(b'\n')
            s.sort()
            return b"\n".join(s)
        self.assertEqual(normalize(ical1), normalize(ical2))
        return ical2

    def verifyICal(self, ical):
        """
        Does a best effort on verifying that the ical is correct, by
        pushing it through the vobject and icalendar library
        """
        vobj = vobject.readOne(to_normal_str(ical))
        icalobj = icalendar.Calendar.from_ical(ical)
        self.assertSameICal(icalobj.to_ical(), ical)
        self.assertSameICal(vobj.serialize(), ical)
        return icalobj.to_ical()
    
    ## TODO: create a test_fix, should be fairly simple - for each
    ## "fix" that's done in the code, make up some broken ical data
    ## that demonstrates the brokenness we're dealing with (preferably
    ## real-world examples). Then ...
    #for bical in broken_ical:
    #    verifyICal(vcal.fix(bical))

    def test_create_ical(self):
        def create_and_validate(**args):
            return self.verifyICal(create_ical(**args))

        ## First, a fully valid ical_fragment should go through as is
        self.assertSameICal(create_and_validate(ical_fragment=ev), ev)

        ## The returned ical_fragment should always contain BEGIN:VCALENDAR and END:VCALENDAR
        ical_fragment = ev.replace('BEGIN:VCALENDAR', '').replace('END:VCALENDAR', '')
        self.assertSameICal(create_and_validate(ical_fragment=ical_fragment), ev)
        
        ## foo bar
        some_ical = create_and_validate(summary="gobledok", dtstart=datetime(2032,10,10,10,10,10, tzinfo=utc), duration=timedelta(hours=5))
        self.assertTrue(b'DTSTART;VALUE=DATE-TIME:20321010T101010Z' in some_ical)
        
        

