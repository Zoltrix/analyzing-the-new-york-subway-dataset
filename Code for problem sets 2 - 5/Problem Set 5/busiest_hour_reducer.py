import sys
import logging



from util import reducer_logfile
from datetime import datetime as dt

logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():
    '''
    Write a reducer that will compute the busiest date and time (that is, the 
    date and time with the most entries) for each turnstile unit. Ties should 
    be broken in favor of datetimes that are later on in the month of May. You 
    may assume that the contents of the reducer will be sorted so that all entries 
    corresponding to a given UNIT will be grouped together.
    
    The reducer should print its output with the UNIT name, the datetime (which 
    is the DATEn followed by the TIMEn column, separated by a single space), and 
    the number of entries at this datetime, separated by tabs.

    For example, the output of the reducer should look like this:
    R001    2011-05-11 17:00:00	   31213.0
    R002	2011-05-12 21:00:00	   4295.0
    R003	2011-05-05 12:00:00	   995.0
    R004	2011-05-12 12:00:00	   2318.0
    R005	2011-05-10 12:00:00	   2705.0
    R006	2011-05-25 12:00:00	   2784.0
    R007	2011-05-10 12:00:00	   1763.0
    R008	2011-05-12 12:00:00	   1724.0
    R009	2011-05-05 12:00:00	   1230.0
    R010	2011-05-09 18:00:00	   30916.0
    ...
    ...

    Since you are printing the output of your program, printing a debug 
    statement will interfere with the operation of the grader. Instead, 
    use the logging module, which we've configured to log to a file printed 
    when you click "Test Run". For example:
    logging.info("My debugging message")
    '''

    max_entries = 0.0
    old_key = None
    datetime = ''
    max_date = ''
    max_time = ''

    for line in sys.stdin:
        data = line.strip().split('\t')
        
        if len(data) != 4:
            continue
            
        this_key, count, date, time = data
        
        count = float(count)
        if old_key and old_key != this_key:
            print '{0}\t{1}\t{2}'.format(old_key, datetime, max_entries)
            max_entries = 0
            datetime = ''
            max_date = ''
            max_time = ''
        
        old_key = this_key
        if count > max_entries:
            max_entries = count
            max_date = date
            max_time = time
            
        elif count == max_entries:
            
            if max_date == '' or max_time == '':
                max_date = date
                max_time = time
                
            else:
                #compare dates
                a = dt.strptime(max_date, '%Y-%m-%d')
                b = dt.strptime(date, '%Y-%m-%d')
                
                
                #compare times
                c = dt.strptime(time, '%H:%M:%S')
                d = dt.strptime(max_time, '%H:%M:%S')
                
                #first compare dates
                if b > a:
                    max_date = date
                    max_time = time
                
                #if dates tie, then compare by time of day
                elif b == a:
                    if c > d:
                        max_time = time
        
        datetime = '{0} {1}'.format(max_date, max_time)
            
    if old_key:
        print '{0}\t{1}\t{2}'.format(old_key, datetime, max_entries)

reducer()
