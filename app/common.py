from typing import Iterator, Optional,Any
import io
import time
from functools import wraps
from datetime import datetime
import sys
import traceback

def clean_csv_value(value: Optional[Any]) -> str:
    if value is None:
        return r'\N'
    return str(value).replace('\n', '\\n')
#Creating a string like an object named CSV file using textio base.

class StringIteratorIO(io.TextIOBase):

    def __init__(self, iter: Iterator[str]):
        self._iterator = iter
        self._buffer = ''
    
    def _initial_read(self, n: Optional[int] = None) -> str:
        while not self._buffer:
            try:
                self._buffer = next(self._iterator)
            except StopIteration:
                break
        ret = self._buffer[:n]
        self._buffer = self._buffer[len(ret):] 
        return ret

    def read(self, n: Optional[int] = None) -> str:
        csv_line = []
        if n is None or n < 0:
            while True:
                m = self._initial_read()
                if not m:
                    break
                csv_line.append(m)
        else:
            while n > 0:
                m = self._initial_read(n)
                if not m:
                    break
                n -= len(m)
                csv_line.append(m)
        # if not any(csv_line) :
        #     raise print("All Values are exist in the actual table")
        return ''.join(csv_line)

#Creating a decorator to measure time required to complete the task
def timeit(fn):
    @wraps(fn)

    def time_delta(*args, **kwargs):
        
        print_msg("""{}()""".format(fn.__name__))

        # Estimating the Time Delta

        start_time = time.perf_counter()
        retval =fn(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time

        print_msg("""Time elapsed is {0:.4}""".format(elapsed_time))
        
    return time_delta

#Printing a message with time stamp
def print_msg(msg:str)-> None:
    '''
    prints message with time stamp
    
    '''
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('%s: %s' % (time_str, msg))   

#Converting unix time stamp to utc timezone
def date_unixtimestamp_gmt(str_val: str) -> str:
    ts = int(str_val)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    

def exception_message(err):
        
        #Created to handle the exceptions
        
        err_type,err_obj,tb = sys.exc_info()
        line_no = tb.tb_lineno
        
        print_msg("ERROR:{err} on line number:{ln}".format(err=err,ln=line_no))
        
        print_msg("Error traceback: {traceback} -- type:{err_type}".format(traceback=traceback.format_exc(),err_type=err_type) ) 
        print_msg(sys.exc_info()[2])
        print_msg(str(err)) 
