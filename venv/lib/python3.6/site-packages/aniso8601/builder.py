# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

from aniso8601.exceptions import (DayOutOfBoundsError,
                                  HoursOutOfBoundsError, ISOFormatError,
                                  LeapSecondError, MidnightBoundsError,
                                  MinutesOutOfBoundsError, RelativeValueError,
                                  SecondsOutOfBoundsError,
                                  WeekOutOfBoundsError, YearOutOfBoundsError)

class BaseTimeBuilder(object):
    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None,
                   DDD=None):
        raise NotImplementedError

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        raise NotImplementedError

    @classmethod
    def build_datetime(cls, date, time):
        raise NotImplementedError

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):
        raise NotImplementedError

    @classmethod
    def build_interval(cls, start=None, end=None, duration=None):
        #start, end, and duration are all tuples
        raise NotImplementedError

    @classmethod
    def build_repeating_interval(cls, R=None, Rnn=None, interval=None):
        #interval is a tuple
        raise NotImplementedError

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        raise NotImplementedError

    @staticmethod
    def cast(value, castfunction, caughtexceptions=(ValueError,),
             thrownexception=ISOFormatError, thrownmessage=None):

        try:
            result = castfunction(value)
        except caughtexceptions:
            raise thrownexception(thrownmessage)

        return result

    @classmethod
    def _build_object(cls, parsetuple):
        #Given a TupleBuilder tuple, build the correct object
        if parsetuple[-1] == 'date':
            return cls.build_date(YYYY=parsetuple[0], MM=parsetuple[1],
                                  DD=parsetuple[2], Www=parsetuple[3],
                                  D=parsetuple[4], DDD=parsetuple[5])
        elif parsetuple[-1] == 'time':
            return cls.build_time(hh=parsetuple[0], mm=parsetuple[1],
                                  ss=parsetuple[2], tz=parsetuple[3])
        elif parsetuple[-1] == 'datetime':
            return cls.build_datetime(parsetuple[0], parsetuple[1])
        elif parsetuple[-1] == 'duration':
            return cls.build_duration(PnY=parsetuple[0], PnM=parsetuple[1],
                                      PnW=parsetuple[2], PnD=parsetuple[3],
                                      TnH=parsetuple[4], TnM=parsetuple[5],
                                      TnS=parsetuple[6])
        elif parsetuple[-1] == 'interval':
            return cls.build_interval(start=parsetuple[0], end=parsetuple[1],
                                      duration=parsetuple[2])
        elif parsetuple[-1] == 'repeatinginterval':
            return cls.build_repeating_interval(R=parsetuple[0],
                                                Rnn=parsetuple[1],
                                                interval=parsetuple[2])

        return cls.build_timezone(negative=parsetuple[0], Z=parsetuple[1],
                                  hh=parsetuple[2], mm=parsetuple[3],
                                  name=parsetuple[4])

class TupleBuilder(BaseTimeBuilder):
    #Builder used to return the arguments as a tuple, cleans up some parse methods
    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None,
                   DDD=None):

        return (YYYY, MM, DD, Www, D, DDD, 'date')

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        return (hh, mm, ss, tz, 'time')

    @classmethod
    def build_datetime(cls, date, time):
        return (date, time, 'datetime')

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):

        return (PnY, PnM, PnW, PnD, TnH, TnM, TnS, 'duration')

    @classmethod
    def build_interval(cls, start=None, end=None, duration=None):
        return (start, end, duration, 'interval')

    @classmethod
    def build_repeating_interval(cls, R=None, Rnn=None, interval=None):
        return (R, Rnn, interval, 'repeatinginterval')

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        return (negative, Z, hh, mm, name, 'timezone')

class PythonTimeBuilder(BaseTimeBuilder):
    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None,
                   DDD=None):

        if YYYY is not None:
            #Truncated dates, like '19', refer to 1900-1999 inclusive,
            #we simply parse to 1900
            if len(YYYY) < 4:
                #Shift 0s in from the left to form complete year
                YYYY = YYYY.ljust(4, '0')

            year = BaseTimeBuilder.cast(YYYY, int,
                                        thrownmessage=
                                        'Invalid year string.')

        if MM is not None:
            month = BaseTimeBuilder.cast(MM, int,
                                         thrownmessage=
                                         'Invalid month string.')
        else:
            month = 1

        if DD is not None:
            day = BaseTimeBuilder.cast(DD, int,
                                       thrownmessage=
                                       'Invalid day string.')
        else:
            day = 1

        if Www is not None:
            weeknumber = BaseTimeBuilder.cast(Www, int,
                                              thrownmessage=
                                              'Invalid week string.')

            if weeknumber == 0 or weeknumber > 53:
                raise WeekOutOfBoundsError('Week number must be between '
                                           '1..53.')
        else:
            weeknumber = None

        if DDD is not None:
            dayofyear = BaseTimeBuilder.cast(DDD, int,
                                             thrownmessage=
                                             'Invalid day string.')
        else:
            dayofyear = None

        if D is not None:
            dayofweek = BaseTimeBuilder.cast(D, int,
                                             thrownmessage=
                                             'Invalid day string.')

            if dayofweek == 0 or dayofweek > 7:
                raise DayOutOfBoundsError('Weekday number must be between '
                                          '1..7.')
        else:
            dayofweek = None

        #0000 (1 BC) is not representable as a Python date so a ValueError is
        #raised
        if year == 0:
            raise YearOutOfBoundsError('Year must be between 1..9999.')

        if dayofyear is not None:
            return PythonTimeBuilder._build_ordinal_date(year, dayofyear)
        elif weeknumber is not None:
            return PythonTimeBuilder._build_week_date(year, weeknumber,
                                                      isoday=dayofweek)

        return datetime.date(year, month, day)

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        #Builds a time from the given parts, handling fractional arguments
        #where necessary
        hours = 0
        minutes = 0
        seconds = 0

        floathours = float(0)
        floatminutes = float(0)
        floatseconds = float(0)

        if hh is not None:
            if '.' in hh:
                floathours = BaseTimeBuilder.cast(hh,
                                                  float,
                                                  thrownmessage=
                                                  'Invalid hour string.')
                hours = 0
            else:
                hours = BaseTimeBuilder.cast(hh,
                                             int,
                                             thrownmessage=
                                             'Invalid hour string.')

        if mm is not None:
            if '.' in mm:
                floatminutes = BaseTimeBuilder.cast(mm,
                                                    float,
                                                    thrownmessage=
                                                    'Invalid minute string.')
                minutes = 0
            else:
                minutes = BaseTimeBuilder.cast(mm,
                                               int,
                                               thrownmessage=
                                               'Invalid minute string.')

        if ss is not None:
            if '.' in ss:
                #Truncate to maximum supported precision
                floatseconds = BaseTimeBuilder.cast(ss[0:ss.index('.') + 7],
                                                    float,
                                                    thrownmessage=
                                                    'Invalid second string.')
                seconds = 0
            else:
                seconds = BaseTimeBuilder.cast(ss,
                                               int,
                                               thrownmessage=
                                               'Invalid second string.')

        #Range checks
        if (hours == 23 and floathours == 0 and minutes == 59
                and floatminutes == 0 and seconds == 60 and floatseconds == 0):
            #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
            raise LeapSecondError('Leap seconds are not supported.')

        if (hours == 24 and floathours == 0
                and (minutes != 0 or floatminutes != 0 or seconds != 0
                     or floatseconds != 0)):
            raise MidnightBoundsError('Hour 24 may only represent midnight.')

        if hours > 24 or floathours > 24:
            raise HoursOutOfBoundsError('Hour must be between 0..24 with '
                                        '24 representing midnight.')

        if minutes >= 60 or floatminutes >= 60:
            raise MinutesOutOfBoundsError('Minutes must be less than 60.')

        if seconds >= 60 or floatseconds >= 60:
            raise SecondsOutOfBoundsError('Seconds must be less than 60.')

        #Fix ranges that have passed range checks
        if hours == 24:
            hours = 0
            minutes = 0
            seconds = 0

        #Datetimes don't handle fractional components, so we use a timedelta
        if tz is not None:
            return (datetime.datetime(1, 1, 1,
                                      hour=hours,
                                      minute=minutes,
                                      second=seconds,
                                      tzinfo=cls._build_object(tz))
                    + datetime.timedelta(hours=floathours,
                                         minutes=floatminutes,
                                         seconds=floatseconds)
                   ).timetz()

        return (datetime.datetime(1, 1, 1,
                                  hour=hours,
                                  minute=minutes,
                                  second=seconds)
                + datetime.timedelta(hours=floathours,
                                     minutes=floatminutes,
                                     seconds=floatseconds)
               ).time()

    @classmethod
    def build_datetime(cls, date, time):
        return datetime.datetime.combine(cls._build_object(date),
                                         cls._build_object(time))

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):
        years = 0
        months = 0
        days = 0
        weeks = 0
        hours = 0
        minutes = 0
        seconds = 0

        if PnY is not None:
            years = BaseTimeBuilder.cast(PnY,
                                         float,
                                         thrownmessage=
                                         'Invalid year string.')

        if PnM is not None:
            months = BaseTimeBuilder.cast(PnM,
                                          float,
                                          thrownmessage=
                                          'Invalid month string.')
        if PnD is not None:
            days = BaseTimeBuilder.cast(PnD,
                                        float,
                                        thrownmessage=
                                        'Invalid day string.')

        if PnW is not None:
            if '.' in PnW:
                weeks = BaseTimeBuilder.cast(PnW,
                                             float,
                                             thrownmessage=
                                             'Invalid week string.')
            else:
                weeks = BaseTimeBuilder.cast(PnW,
                                             int,
                                             thrownmessage=
                                             'Invalid week string.')

        if TnH is not None:
            if '.' in TnH:
                hours = BaseTimeBuilder.cast(TnH,
                                             float,
                                             thrownmessage=
                                             'Invalid hour string.')
            else:
                hours = BaseTimeBuilder.cast(TnH,
                                             int,
                                             thrownmessage=
                                             'Invalid hour string.')

        if TnM is not None:
            if '.' in TnM:
                minutes = BaseTimeBuilder.cast(TnM,
                                               float,
                                               thrownmessage=
                                               'Invalid minute string.')
            else:
                minutes = BaseTimeBuilder.cast(TnM,
                                               int,
                                               thrownmessage=
                                               'Invalid minute string.')

        if TnS is not None:
            if '.' in TnS:
                #Truncate to maximum supported precision
                seconds = BaseTimeBuilder.cast(TnS[0:TnS.index('.') + 7],
                                               float,
                                               thrownmessage=
                                               'Invalid second string.')
            else:
                seconds = BaseTimeBuilder.cast(TnS,
                                               int,
                                               thrownmessage=
                                               'Invalid second string.')

        #Note that weeks can be handled without conversion to days
        totaldays = years * 365 + months * 30 + days

        return datetime.timedelta(days=totaldays,
                                  seconds=seconds,
                                  minutes=minutes,
                                  hours=hours,
                                  weeks=weeks)

    @classmethod
    def build_interval(cls, start=None, end=None, duration=None):
        if end is not None and duration is not None:
            #<duration>/<end>
            endobject = cls._build_object(end)
            durationobject = cls._build_object(duration)

            if end[-1] == 'date' and (duration[4] is not None
                                      or duration[5] is not None
                                      or duration[6] is not None):
                #<end> is a date, and <duration> requires datetime resolution
                return (endobject,
                        cls.build_datetime(end, TupleBuilder.build_time())
                        - durationobject)

            return (endobject,
                    endobject
                    - durationobject)
        elif start is not None and duration is not None:
            #<start>/<duration>
            startobject = cls._build_object(start)
            durationobject = cls._build_object(duration)

            if start[-1] == 'date' and (duration[4] is not None
                                        or duration[5] is not None
                                        or duration[6] is not None):
                #<start> is a date, and <duration> requires datetime resolution
                return (startobject,
                        cls.build_datetime(start, TupleBuilder.build_time())
                        + durationobject)

            return (startobject,
                    startobject
                    + durationobject)

        #<start>/<end>
        startobject = cls._build_object(start)
        endobject = cls._build_object(end)

        return (startobject, endobject)

    @classmethod
    def build_repeating_interval(cls, R=None, Rnn=None, interval=None):
        startobject = None
        endobject = None

        if interval[0] is not None:
            startobject = cls._build_object(interval[0])

        if interval[1] is not None:
            endobject = cls._build_object(interval[1])

        if interval[2] is not None:
            durationobject = cls._build_object(interval[2])
        else:
            durationobject = endobject - startobject

        if R is True:
            if startobject is not None:
                return cls._date_generator_unbounded(startobject,
                                                     durationobject)

            return cls._date_generator_unbounded(endobject,
                                                 -durationobject)

        iterations = BaseTimeBuilder.cast(Rnn, int,
                                          thrownmessage='Invalid iterations.')

        if startobject is not None:
            return cls._date_generator(startobject, durationobject, iterations)

        return cls._date_generator(endobject, -durationobject, iterations)

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        if Z is True:
            #Z -> UTC
            return UTCOffset(name='UTC', minutes=0)

        if hh is not None:
            tzhour = BaseTimeBuilder.cast(hh, int,
                                          thrownmessage=
                                          'Invalid hour string.')
        else:
            tzhour = 0

        if mm is not None:
            tzminute = BaseTimeBuilder.cast(mm, int,
                                            thrownmessage=
                                            'Invalid minute string.')
        else:
            tzminute = 0

        if negative is True:
            return UTCOffset(name=name, minutes=-(tzhour * 60 + tzminute))

        return UTCOffset(name=name, minutes=tzhour * 60 + tzminute)

    @staticmethod
    def _build_week_date(isoyear, isoweek, isoday=None):
        if isoday is None:
            return (PythonTimeBuilder._iso_year_start(isoyear)
                    + datetime.timedelta(weeks=isoweek - 1))

        return (PythonTimeBuilder._iso_year_start(isoyear)
                + datetime.timedelta(weeks=isoweek - 1, days=isoday - 1))

    @staticmethod
    def _build_ordinal_date(isoyear, isoday):
        #Day of year to a date
        #https://stackoverflow.com/questions/2427555/python-question-year-and-day-of-year-to-date
        builtdate = (datetime.date(isoyear, 1, 1)
                     + datetime.timedelta(days=isoday - 1))

        #Enforce ordinal day limitation
        #https://bitbucket.org/nielsenb/aniso8601/issues/14/parsing-ordinal-dates-should-only-allow
        if isoday == 0 or builtdate.year != isoyear:
            raise DayOutOfBoundsError('Day of year must be from 1..365, '
                                      '1..366 for leap year.')

        return builtdate

    @staticmethod
    def _iso_year_start(isoyear):
        #Given an ISO year, returns the equivalent of the start of the year
        #on the Gregorian calendar (which is used by Python)
        #Stolen from:
        #http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar

        #Determine the location of the 4th of January, the first week of
        #the ISO year is the week containing the 4th of January
        #http://en.wikipedia.org/wiki/ISO_week_date
        fourth_jan = datetime.date(isoyear, 1, 4)

        #Note the conversion from ISO day (1 - 7) and Python day (0 - 6)
        delta = datetime.timedelta(days=fourth_jan.isoweekday() - 1)

        #Return the start of the year
        return fourth_jan - delta

    @staticmethod
    def _date_generator(startdate, timedelta, iterations):
        currentdate = startdate
        currentiteration = 0

        while currentiteration < iterations:
            yield currentdate

            #Update the values
            currentdate += timedelta
            currentiteration += 1

    @staticmethod
    def _date_generator_unbounded(startdate, timedelta):
        currentdate = startdate

        while True:
            yield currentdate

            #Update the value
            currentdate += timedelta

class RelativeTimeBuilder(PythonTimeBuilder):
    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):

        try:
            import dateutil.relativedelta
        except ImportError:
            raise RuntimeError('dateutil must be installed for '
                               'relativedelta support.')

        if ((PnY is not None and '.' in PnY)
                or (PnM is not None and '.' in PnM)):
            #https://github.com/dateutil/dateutil/issues/40
            raise RelativeValueError('Fractional months and years are not '
                                     'defined for relative durations.')

        years = 0
        months = 0
        days = 0
        weeks = 0
        hours = 0
        minutes = 0
        seconds = 0
        microseconds = 0

        if PnY is not None:
            years = BaseTimeBuilder.cast(PnY,
                                         int,
                                         thrownmessage=
                                         'Invalid year string.')

        if PnM is not None:
            months = BaseTimeBuilder.cast(PnM,
                                          int,
                                          thrownmessage=
                                          'Invalid month string.')

        if PnD is not None:
            days = BaseTimeBuilder.cast(PnD,
                                        float,
                                        thrownmessage=
                                        'Invalid day string.')

        if PnW is not None:
            if '.' in PnW:
                weeks = BaseTimeBuilder.cast(PnW,
                                             float,
                                             thrownmessage=
                                             'Invalid week string.')
            else:
                weeks = BaseTimeBuilder.cast(PnW,
                                             int,
                                             thrownmessage=
                                             'Invalid week string.')

        if TnH is not None:
            if '.' in TnH:
                hours = BaseTimeBuilder.cast(TnH,
                                             float,
                                             thrownmessage=
                                             'Invalid hour string.')
            else:
                hours = BaseTimeBuilder.cast(TnH,
                                             int,
                                             thrownmessage=
                                             'Invalid hour string.')

        if TnM is not None:
            if '.' in TnM:
                minutes = BaseTimeBuilder.cast(TnM,
                                               float,
                                               thrownmessage=
                                               'Invalid minute string.')
            else:
                minutes = BaseTimeBuilder.cast(TnM,
                                               int,
                                               thrownmessage=
                                               'Invalid minute string.')

        if TnS is not None:
            if '.' in TnS:
                #Split into seconds and microseconds
                seconds = BaseTimeBuilder.cast(TnS[0:TnS.index('.')],
                                               int,
                                               thrownmessage=
                                               'Invalid second string.')

                #Truncate to maximum supported precision
                microseconds = (BaseTimeBuilder.cast(TnS[TnS.index('.'):
                                                         TnS.index('.') + 7],
                                                     float,
                                                     thrownmessage=
                                                     'Invalid second string.')
                                * 1e6)
            else:
                seconds = BaseTimeBuilder.cast(TnS,
                                               int,
                                               thrownmessage=
                                               'Invalid second string.')

        return dateutil.relativedelta.relativedelta(years=years,
                                                    months=months,
                                                    weeks=weeks,
                                                    days=days,
                                                    hours=hours,
                                                    minutes=minutes,
                                                    seconds=seconds,
                                                    microseconds=microseconds)

class UTCOffset(datetime.tzinfo):
    def __init__(self, name=None, minutes=None):
        #We build an offset in this manner since the
        #tzinfo class must have an init
        #"method that can be called with no arguments"
        self._name = name

        if minutes is not None:
            self._utcdelta = datetime.timedelta(minutes=minutes)
        else:
            self._utcdelta = None

    def __repr__(self):
        if self._utcdelta >= datetime.timedelta(hours=0):
            return '+{0} UTC'.format(self._utcdelta)

        #From the docs:
        #String representations of timedelta objects are normalized
        #similarly to their internal representation. This leads to
        #somewhat unusual results for negative timedeltas.

        #Clean this up for printing purposes
        #Negative deltas start at -1 day
        correcteddays = abs(self._utcdelta.days + 1)

        #Negative deltas have a positive seconds
        deltaseconds = (24 * 60 * 60) - self._utcdelta.seconds

        #(24 hours / day) * (60 minutes / hour) * (60 seconds / hour)
        days, remainder = divmod(deltaseconds, 24 * 60 * 60)

        #(1 hour) * (60 minutes / hour) * (60 seconds / hour)
        hours, remainder = divmod(remainder, 1 * 60 * 60)

        #(1 minute) * (60 seconds / minute)
        minutes, seconds = divmod(remainder, 1 * 60)

        #Add any remaining days to the correcteddays count
        correcteddays += days

        if correcteddays == 0:
            return '-{0}:{1:02}:{2:02} UTC'.format(hours, minutes, seconds)
        elif correcteddays == 1:
            return '-1 day, {0}:{1:02}:{2:02} UTC'.format(hours,
                                                          minutes,
                                                          seconds)

        return '-{0} days, {1}:{2:02}:{3:02} UTC'.format(correcteddays,
                                                         hours,
                                                         minutes,
                                                         seconds)

    def utcoffset(self, dt):
        return self._utcdelta

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        #ISO 8601 specifies offsets should be different if DST is required,
        #instead of allowing for a DST to be specified
        # https://docs.python.org/2/library/datetime.html#datetime.tzinfo.dst
        return datetime.timedelta(0)
