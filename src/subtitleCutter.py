
from itertools import groupby
from datetime import datetime

def trimSRTfile(infilename,outfilename,sliceStart,sliceEnd):

  n=0
  tszero = datetime.strptime('00:00:00,000', '%H:%M:%S,%f')

  with open(outfilename,'w') as outfile:
    outfile.write('')
    for key,grp in groupby(open(infilename,'rb').readlines(),key=lambda x:x.strip()!=b''):
      try:
        if key:
          lstgrp = [x.decode('utf8',errors="ignore") for x in list(grp)] 
          
          number,timestamp,*lines = lstgrp 
          print(number,timestamp)

          tsstart,tsend =  timestamp.split(' --> ')
          
          tsstart = tsstart.strip()
          tsend = tsend.strip()

          tsstart = datetime.strptime(tsstart, '%H:%M:%S,%f')
          tsend   = datetime.strptime(tsend, '%H:%M:%S,%f')


          tsstart = (tsstart-tszero).total_seconds()
          tsend   = (tsend-tszero).total_seconds()

          if not (tsend<sliceStart or tsstart>sliceEnd):
            n+=1
            tsstart = max(tsstart,sliceStart)-sliceStart
            tsend   = min(tsend,sliceEnd)-sliceStart

            if tsstart==0:
              tsstart+=0.1

            tsstart_str = datetime.strftime(datetime.utcfromtimestamp(tsstart),'%H:%M:%S,%f')          
            startP1,startP2 = tsstart_str.split(',')
            tsstart_str = startP1 + ',' + str(int(int(startP2)/1000)).zfill(3)

            tsend_str   = datetime.strftime(datetime.utcfromtimestamp(tsend),'%H:%M:%S,%f')
            startP2,endP2 = tsend_str.split(',')
            tsend_str = startP2 + ',' + str(int(int(endP2)/1000)).zfill(3)


            timeString = "{}\n{} --> {}\n{}\n".format(n,
              tsstart_str,
              tsend_str,
              '\n'.join(lines)
            )

            outfile.write(timeString)
      except Exception as e:
        print(e)
    if n == 0:
      outfile.write("1\n00:00:00,000 --> 00:00:00,000\n\n")