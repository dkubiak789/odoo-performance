#!/usr/bin/python
# performance_test.py by Dariusz Kubiak

import time, random

class Performance(object):

    def __init__(self, **kwargs):
        self.action_interval = kwargs.get('action_interval', 2)
        self._debug_mode = kwargs.pop('debug', False)
        self._last_time = time.time()
        self._last_action = time.time()
        self.properties = kwargs

        file_name = kwargs.pop('file_name', '/var/log/openerp/openerp-performance-test.log')
        self.log_file = open(file_name,'a+')


    def __del__(self):
        self.log_file.close()


    @property
    def check_point(self):
        return self.properties.get('check_point', None)


    @check_point.setter
    def check_point(self, cp):
        if not cp: return
        if self._debug_mode:
            print "check_point: %s (%.4f s)." % (cp, self.properties.get(cp, 0.0))

        if not self.properties.has_key(cp):
            self.properties[cp] = 0

        self.properties[cp] += time.time() - self._last_time
        self._last_time = time.time()


    @check_point.deleter
    def check_point(self):
        print "check_point deleter"
        del self.properties['check_point']


    def results(self):
        for k,v in self.properties.items():
            print "%s took %.4f seconds" % (k, self.properties[k])


    def interval_action(self, **kwargs):
        if time.time() - self._last_action < self.action_interval:
            return
        self._last_action = time.time()

        index = kwargs.get('index', 0)
        total_items = kwargs.get('total_items', 0)

        log_line = ""
        if index and total_items:
            log_line += "Processed %s of %s claims" % (index, total_items)

        for k,v in self.properties.items():
            log_line += ", %s: %.4f s" % (k, self.properties[k])

        print "line: %s" % log_line
        self.log_file.write(time.strftime("%Y-%m-%d %H:%M:%S") + ' ' + log_line + '\n')



def main():

    items_lst = range(5)

    # p = Performance()
    p = Performance(debug = True)

    for i, claim in enumerate(items_lst):

        p.interval_action(index=i, total_items=len(items_lst))

        time.sleep(random.randint(0, 1))
        p.check_point = 'Quick'

        time.sleep(random.randint(2, 3))
        p.check_point = 'Slow'

    p.results()


if __name__ == "__main__": main()
