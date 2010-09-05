import os
import sys

def chunk_report( bytes_so_far, chunk_size, total_size ):
        percent = float(bytes_so_far) / total_size
        percent = round(percent*100, 2)

        sys.stdout.write( "Downloaded %d of %d bytes (%0.2f%%)\r" %
                (bytes_so_far, total_size, percent) )

        if bytes_so_far >= total_size:
                sys.stdout.write('\n')



def chunk_read( response, fileName, chunk_size=8192, report_hook=None ):
        total_size = int( response.info().getheader('Content-Length').strip() )
        bytes_so_far = 0

        if os.path.exists( fileName ) and os.path.getsize( fileName ) == total_size:
                print "File exists, skip."
                sys.exit(1)

        fp = open( fileName, "wb" )

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
        return bytes_so_far
