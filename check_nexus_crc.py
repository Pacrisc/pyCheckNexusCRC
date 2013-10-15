#!/usr/bin/python
import subprocess, sys, getopt, re

# Set initial values 
community = ''
host = ''
snmpget = '/usr/bin/snmpget'
OID = '.1.3.6.1.2.1.2.2.1.14.'

# Main application 
def main(argv):

    global community
    global host

    # single interface OID to be checked for this version
    interface = '436236288'

    # Verify and Process the command line arguments and print a error message 
    try: 
        opts, args = getopt.getopt(argv, "c:h:",["community=","host=","help"]) 
    except getopt.GetoptError:
        print "\n\n  Invalid Syntax \n  syntax is \'pyCheckNexusCRC.py -c <community>\' \n\n"
        sys.exit(2)

    # Set the globals based on arguments 
    for opt, arg in opts:
        # Help information
        if opt == '--help':
                print 'pyCheckNexusCRC.py -c <community>'
                sys.exit()
        elif opt in ("-c", "--community"):
            community = arg
        elif opt in ("-h", "--host"):
            host = arg
    # get quanity CRC errros on a givin single interface
    print getErrorsOnIf(interface)

# Function which returns CRC error counts via snmp from nexus switches
# accepts interface OID's and uses globals for arguments
def getErrorsOnIf(interface):
    
    #Regex to match the return value of snmpget
    reErrors = re.compile('IF-MIB::ifInErrors.(\d+) = Counter32: (\d+)')
    
    # Runs snmpget, returns stdout & stderr and checks the return code
    p = subprocess.Popen([
        snmpget, 
        '-v', 
        '2c', 
        '-c', 
        community, 
        host, 
        OID+interface ], stderr = subprocess.PIPE, stdout = subprocess.PIPE)
    returnCode = p.wait()
    (stdout, stderr) =  p.communicate()

    # If executed properly, matches error count and returns value
    if returnCode == 0:
        Errors = reErrors.match(stdout).group(2)
        return Errors
    # Returns Critical and strerr if anything other than returnCode 0
    else:
        print 'CRITICAL: '+stderr
        sys.exit()


# Runs the main function if this file is not loaded as a module.
if __name__ == "__main__":
        main(sys.argv[1:])
