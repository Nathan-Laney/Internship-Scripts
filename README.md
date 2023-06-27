# Internship-Scripts
Scripts created for my Cybersecurity Analyst internship. 

## NTLMv1-Compiler-v2.py
This script runs on Windows Event log files in order to find login events using NTLMv1 in order to trace back their source devices in environments with large log quantities. 

Put your filepath of your log file in the open() at the top. Windows, MacOS and Linux can all use / instead of \.

Run the script. The output in console will show you how many lines have been processed so far, and will print the output when completed. Control-C will end the script early and print in console all findings so far. 

Tested on multiple log files of 12GB in size each, successfully scanning almost 300 million lines of logs per file. Allowed us to find and repair vulnerable devices still using NTLMv1.  

## Remove-DisabledUserGroup.ps1
This script was designed to automatically detect and remove permissions from members of the 'Disabled-Users' OU on a Windows Azure Active Directory based ecosystem. This script was scheduled with Task Scheduler to execute once per day. 

To use this script, modify the variables $DC_IP, $USERS_TO_REMOVE, and $OU_TO_IGNORE. 

$DC_IP should be set to the IP address of the DC on your network that you wish to modify. 

$USERS_TO_REMOVE should be set to the Disabled Users OU, or whatever OU you wish to remove permissions of. 

$OU_TO_IGNORE should be set to an OU you wish to protect from automatic stripping of credentials. For our use case, there was a group that required manual population of their credentials, so we ignore them in this script as it is run daily and instead have a seperate script to remove their permissions less often. 

*This script will not modify your active directory unless the -WhatIf flag on line 79 is removed.* 

This tag ensures the script only logs, rather than executes. After you are content with your testing of this script, you can remove this tag and it will begin implementing its changes. 