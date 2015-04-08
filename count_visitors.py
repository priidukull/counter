import argparse
import csv
from datetime import timedelta, datetime
from operator import itemgetter


def asstring(time):
    return time.strftime('%H:%M')


def astime(timestr):
    return datetime.strptime(timestr, '%H:%M').time()


def plus_minute(current):
    current = datetime.combine(datetime.now().date(), current)
    current += timedelta(minutes=1)
    return current.time()


def exit_program(e):
    print(e)
    exit()


class Main:
    def __init__(self, args):
        super().__init__()
        self.fname = args.fname
        self.open = args.open
        self.close = args.close
        self.sort_by_count = args.sort_by_count
        self.visits = []
        self.visitor_counts = {}
        self.period_counts = []
        self.row_number = None
        self.illegal_inputs = []

    def _read_input(self):
        try:
            self._read_from_file()

        except FileNotFoundError as e:
            exit_program(e)

    def _read_from_file(self):
        with open(self.fname, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            self.row_number = 0
            for row in reader:
                self.row_number += 1
                try:
                    self._read_visit(row)

                except ValueError as e:
                    self.illegal_inputs.append(
                        'Could not parse input from line %s of %s: %s, %s' % \
                        (self.row_number, self.fname, row, e))

    def _read_visit(self, row):
        start, end = row
        start, end = astime(start), astime(end)
        if start > end:
            raise ValueError('End time %s before start time %s' % (end, start))
        self.visits.append((start, end))

    def _aggregate_visitor_counts(self):
        for start, end in self.visits:
            current = start
            while current <= end:
                self.visitor_counts[current] = self.visitor_counts.get(current, 0) + 1
                current = plus_minute(current)

    def _aggregate_period_counts(self):
        visit_times = set(self.visitor_counts)
        visit_times.update({t for t in [self.open, self.close] if t})
        opened, closed = min(visit_times), max(visit_times)

        p_start, p_end = None, None
        p_count = self.visitor_counts.get(opened, 0)
        current = opened

        def append_last_period():
            period = '%s-%s' % (asstring(p_start), asstring(p_end))
            self.period_counts.append((period, p_count))

        while not current > closed:
            p_start = p_start or current
            count = self.visitor_counts.get(current, 0)
            if p_count != count:
                append_last_period()
                p_count = count
                p_start = None

            p_start = p_start or current
            p_end = current
            current = plus_minute(current)

        else:
            append_last_period()

    def _print_output(self):
        if self.sort_by_count:
            self.period_counts = sorted(self.period_counts, key=itemgetter(1), reverse=True)

        for period, count in self.period_counts:
            print(period, count)

        for m in self.illegal_inputs:
            print(m)

    def main(self):
        try:
            self.open = astime(self.open) if self.open else None
            self.close = astime(self.close) if self.close else None

        except ValueError as e:
            exit_program(e)

        self._read_input()
        self._aggregate_visitor_counts()
        self._aggregate_period_counts()
        self._print_output()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='fname', required=True, help='Path to the input file')
    parser.add_argument('-o', dest='open', help='The time when the doors are opened. Defaults to None. Format <H:MM>, for example 8:34')
    parser.add_argument('-c', dest='close', help='The time when the doors are closed. Defaults to None. Format <H:MM>, for example 8:34')
    parser.add_argument('--sort_by_count', action='store_true', help='Sort output by visitor count. If argument is not present, the output will be sorted by time')
    args = parser.parse_args()

    Main(args).main()