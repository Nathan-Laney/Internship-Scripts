# NTLMv1 Login Finder

# Tool to parse Windows Event Log files to detect NTLMv1 login events. 
# Ignores login events of 'ANONYMOUS LOGON', as they do not reflect security risks in this context. 
# For more information about NTLMv1 and why it is a risk:
# https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/audit-domain-controller-ntlmv1

# Nathan Laney 
# June 6 2023
# Written on Python v. 3.11


import os
from collections import defaultdict


file1 = open("INSERT LOG FILE PATH HERE", 'r')
# Count is how many lines were read
count = 0
# logonCount is how many login events have been detected 
logonCount = 0
# Variable used to scrap outputs of anonymous logins
keep = True

# NTLM_V1_LoginInfo is the dictionary that holds the output. 
# The key is the workstation name or account name, depending on which lines are commented out
# The value is the unique IP addresses from which the logins using NTLMv1 were attempted. 
NTLM_V1_LoginInfo = defaultdict(set)

# I am aware this is not the fastest way to perform these checks, but the script was written to be run
# on log files stored on a network drive, and as such it doesn't matter as network speed is by far
# the speed limiter on this script. Script still works on local files just fine, though
try:
    while True:
        count += 1
    
        # Get next line from file
        line = file1.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break

        # Logon event starts
        elif "New Logon:" in line:
            keep = True
            logonCount += 1

######################## CHOOSE ONE OR THE OTHER ########################

        # (OPTION 1)
        # Grab PC Workstation name 

        elif "Workstation Name:" in line:
            strippedLine = line.strip()
            wsName = strippedLine[17:].strip()

        # (OPTION 2)
        # Grab logon account name instead of workstation name 

        # elif "Account Name:" in line:
        #     strippedLine = line.strip()
        #     wsName = strippedLine[13:].strip()

#########################################################################
           
        
        elif "Source Network Address:" in line:
            # Stores stripped IP address of logon attempt source
            strippedLine = line.strip()
            sna = strippedLine[23:].strip()
        
        elif "Account Name:		ANONYMOUS LOGON" in line:
            keep = False
        
        elif "NTLM V1" in line:
            if keep:
                NTLM_V1_LoginInfo[wsName].add(sna)
                # NTLM_V1_LoginInfo['LogLine'].add(count)

        # Log line meaning login event reporting has ended
        elif "This event is generated when a logon session is created. It is generated on the computer that was accessed." in line:
            keep = True
        
        if (count % 1000000 == 0):
            print("Processed %i million lines." % (count / 1000000))

    file1.close()
    print("Processed %i login attempts." % logonCount)
    print(NTLM_V1_LoginInfo)
except KeyboardInterrupt:
    file1.close()
    print("Processed %i login attempts." % logonCount)
    print(NTLM_V1_LoginInfo)
    pass
