# MS-GSP - Multiple-Support Generalized Sequential Patterns
An implementation of Multi-Support Generalized Sequential Patterns (MS-GSP) algorithm in python.

It can extract frequent patterns from a set of input sequences. MS-GSP is introduced in the following book for mining sequential patterns:

Bing Liu, ["Web Data Mining - Exploring Hyperlinks, Contents, and Usage Data"](https://www.springer.com/us/book/9783642194597), P 43-49, Springer, 2011.

## Files

fileRead.py - Used for reading inputs from data and parameter files. Path to root folder containing these files need to be specified here.

algo_def.py - Contains helper methods

MScandidate_gen_SPM.py - Used for generating candidates

MS-GSP.py - Contains the major portion of the algorithm, including writing the output to the file

## RUN

Copy the input data to "data.txt" file and the parameters to the "para.txt" file

Required: Python 2.7 or Python 3.5.1

Run Ms-GSP.py file in the above environment, providing appropriate inputs(data, parameters).

The result will be written to the "output.txt" file that gets generated in the root folder.
 
