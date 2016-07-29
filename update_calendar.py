import sys, csv, getopt, codecs, datetime
from collections import OrderedDict

class Day(object):

   def __init__(self, date, distance):
      self.date = date
      self.distance = distance

   def csv_day(self):
      return [self.date, self.distance]

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
      print "Date,Distance"
      for date, entry in OrderedDict(sorted(output.items(), key=lambda t: t[0])).items():
         csv_day = entry.csv_day()
         if csv_day != None: #idk why
            print "{0},{1}".format(csv_day[0], csv_day[1])

if __name__ == "__main__":
   main(sys.argv[1:])