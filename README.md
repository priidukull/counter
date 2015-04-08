# Visitor Counter

### Purpose

Visitor Counter is a single file Python script which reads data about each visit and calculates, how many visitors there were in the place on any given minute.

### Input

    -h, --help       show this help message and exit. REQUIRED
    -f FNAME         Path to the input file
    -o OPEN          The time when the doors are opened. Defaults to None. Format <H:MM>, for example 8:34
    -c CLOSE         The time when the doors are closed. Defaults to None. Format <H:MM>, for example 8:34
    --sort_by_count  Sort output by visitor count. If argument is not present,
                     the output will be sorted by time

The input file should be a CSV file in the format <start time>,<end time>. For example: 
    
    9:53,10:03
    8:32,8:37
    
### Output

The script will aggregate the input data and produce periods of time when the number of visits is unchanged and the number of visitors during each period.

The output is given in format {start time(H:MM)}-{end time(H:MM)} {number of visits(d+)}. For example:
   
    8:32-8:37 1
    8:38-9:52 0
    9:53-10:03 1
    
### Arguments open and close
 
By default, the script will calculate the number of visitors for the period between the arrival of the first visitor until the departure of the last visitor. 

Arguments open (-o) and close (-c) may be used to change that behavior. 

If the value of open (-o) is a time earlier than the arrival of the first visitor, then the number of visitors will be calculated starting from the time set by the argument open (-o). Correspondingly, if the value of close (-c) is a time later than the departure of the last visitor, then the number of visitors will be calculated until the time set by the argument close (-c). Essentially, by using the argument open (-o) or close (-c) it is possible to add a period of 0 visitors either to the time before the arrival of the first visitor or after the departure of the last visitor. 

The purpose of the open and close arguments is to enable the output to also show that there was a period of time when the place had been opened to the public and no one had come yet or everyone had left already.

If value of open (-o) is a time later than the first visitor came or the value of close (-c) is a time before the last visitor left, then the argument will be ignored by the program.
    
### Illegal input handling

Argument fname must point to an existing file. Otherwise the program will exist.

Arguments open and close must be legal times in the format {H:MM}. Otherwise the program will exit.

Any line in the CSV file that could not be read by the parser will be ignored. Info about each ignored line will be printed at the end of the output. An example:

    Could not parse input from line 3 of visits.csv: ['09:37', '09:46', '10:00'], too many values to unpack (expected 2)
    

