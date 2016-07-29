import sys, csv, getopt, codecs, datetime
from collections import OrderedDict

class WorldStats(object):

   def __init__(self, per_diem, car_epoch):
      self.distance = 0
      self.per_diem = per_diem
      self.car_epoch = car_epoch

class Day(object):

   def __init__(self, date, cum_used, cum_allotted):
      self.date = date
      self.cum_used = cum_used
      self.cum_allotted = cum_allotted

   def csv_day(self):
      return [self.date, self.cum_used, self.cum_allotted]

def get_date(entry):
   date_str = entry.split(';')[1]
   date = datetime.datetime.strptime(date_str, "%m/%d/%y").date()
   return date

def get_distance(entry):
   return float(entry.split(';')[2])

def parse_csv(inputfile):
   reader = csv.reader(codecs.open(inputfile,'rU','utf-16'))
   per_diem = 10000/365
   car_epoch = datetime.date(2016, 7, 8)
   stats = WorldStats(per_diem, car_epoch)
   journal = {}
   contents = []
   for line in reader:
      contents.append(line)
   for line in reversed(contents):
      distance = 0
      if len(line) == 1:
         continue
      date = get_date(line[0])
      try:
         distance = get_distance(line[4])
      except:
         pass
      stats.distance += distance
      cum_allotted = (date - stats.car_epoch).days * stats.per_diem
      if date in journal:
         journal[date].cum_used += distance
      else:
         journal[date] = Day(date, stats.distance, cum_allotted)

   return journal

def main(argv):
   inputfile = ''
   outputfile = ''
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
   print "Date,Used,Allotted"
   for date, entry in OrderedDict(sorted(output.items(), key=lambda t: t[0])).items():
      csv_day = entry.csv_day()
      if csv_day != None: #idk why
         #pass
         print "{0},{1},{2}".format(csv_day[0], csv_day[1], csv_day[2])

if __name__ == "__main__":
   main(sys.argv[1:])