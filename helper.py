import os
import sys
import multiprocessing
import urllib2

def chunk_report( bytes_so_far, chunk_size, total_size ):
        percent = float(bytes_so_far) / total_size
        percent = round(percent*100, 2)

        sys.stdout.write( "Downloaded %d of %d bytes (%0.2f%%)\r" %
                (bytes_so_far, total_size, percent) )

        if bytes_so_far >= total_size:
                sys.stdout.write('\n')



def chunk_read( fileInfo, chunk_size=8192, report_hook=None ):
	response = urllib2.urlopen(fileInfo[1])
        total_size = int( response.info().getheader('Content-Length').strip() )
        bytes_so_far = 0

        if os.path.exists(fileInfo[0]) and os.path.getsize(fileInfo[0]) == total_size:
                print "File exists, skip."
                sys.exit(1)

        fp = open( fileInfo[0], "wb" )

	print "Starting a job..."

        while True:
                chunk = response.read(chunk_size)
                bytes_so_far += len(chunk)

                if not chunk:
                        break
                else:
                        #write back
                        fp.write( chunk )

		if report_hook:
                        report_hook(bytes_so_far, chunk_size, total_size)

        fp.close()
	print "Finished:", fileInfo[0].split('/',1)[1]
        return bytes_so_far


#fileList: [(name,response),...]
def Download( fileList, numProc ):
    WorkerPool = multiprocessing.Pool(processes=numProc)
    WorkerPool.map( chunk_read, fileList )
