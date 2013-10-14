#!/usr/bin/python
import subprocess, sys, getopt


def main(argv):
    community = ''
    host = ''

    try: 
        opts, args = getopt.getopt(argv, "c:h:",["community=","host=","help"]) 
    except getopt.GetoptError:
        print "\n\n  Invalid Syntax \n  syntax is \'pyCheckNexusCRC.py -c <community>\' \n\n"
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '--help':
                print 'pyCheckNexusCRC.py -c <community>'
                sys.exit()
        elif opt in ("-c", "--community"):
            community = arg
        elif opt in ("-h", "--host"):
            host = arg

    
    print 'Community: ', community
    print 'Host: ', host     
	
    print "OK - the CRC errors are low";

    p = subprocess.Popen('snmpwalk -v 2c -c '+community+' '+host+' .1.3.6.1.2.1.2.2.1.14.436236288', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
        retval = p.wait()

if __name__ == "__main__":
        main(sys.argv[1:])
