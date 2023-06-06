# Internship-Scripts
Scripts created for my Cybersecurity Analyst internship. 

## NTLMv1-Compiler-v2.py
This script runs on Windows Event log files in order to find login events using NTLMv1 in order to trace back their source devices in environments with large log quantities. 
Put your filepath of your log file in the open() at the top. Windows, MacOS and Linux can all use / instead of \. 
Run the script. The output in console will show you how many lines have been processed so far, and will print the output when completed. Control-C will end the script early and print in console all findings so far. 
Tested on multiple log files of 12GB in size each, successfully scanning almost 300 million lines of logs per file. Allowed us to find and repair vulnerable devices still using NTLMv1.  
