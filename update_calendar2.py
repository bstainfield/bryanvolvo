import sys, csv, getopt, codecs, datetime
from collections import OrderedDict
from operator import itemgetter

week_zero = datetime.date(2016, 7, 8)

class Day(object):

   def __init__(self, date, distance):
      self.date = date
      self.distance = distance

   def get_week(self):
      monday1 = (week_zero - datetime.timedelta(days=week_zero.weekday()))
      monday2 = (self.date - datetime.timedelta(days=self.date.weekday()))
      return ((monday2 - monday1).days / 7)+1

   def get_day(self):
      return self.date.isoweekday()

   def csv_day(self):
      #[day, week, distance]
      return [self.get_day(), self.get_week(), self.distance]

def get_ordered_list(items):
   entries = []
   for i in items:
      entries.append(i[1].csv_day())
   return sorted(entries, key=itemgetter(0))

def get_date(entry):
   date_str = entry.split(';')[1]
   date = datetime.datetime.strptime(date_str, "%m/%d/%y").date()
   return date

def get_distance(entry):
   return float(entry.split(';')[2])

def parse_csv(inputfile):
   reader = csv.reader(codecs.open(inputfile,'rU','utf-16'))
   journal = {}
   for line in reader:
      distance = 0
      if len(line) == 1:
         continue
      date = get_date(line[0])
      try:
         distance = get_distance(line[4])
      except:
         pass
      if date in journal:
         journal[date].distance += distance
      else:
         journal[date] = Day(date, distance)

   return journal

def main(argv):
   inputfile = ''
   outputfile = ''
   verbose = False
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'tripcsv.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'tripcsv.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   output = parse_csv(inputfile)
   if verbose:
      for date, entry in output.items():
         print date, ": ", entry.displayDay()
   else:
      print "Day,Week,Distance"
      for entry in get_ordered_list(output.items()):
         print "{0},{1},{2}".format(entry[0],entry[1],entry[2])

if __name__ == "__main__":
   main(sys.argv[1:])