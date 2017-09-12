import logging
import sched

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s = sched.scheduler()

def print_time(a='default'):
    logging.warning(f'From print_time {a}')

logging.warning('Starting...')
s.enter(10, 1, print_time)
s.enter(5, 2, print_time, argument=('postional', ))
s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
s.run()
logging.warning('Exiting...')
