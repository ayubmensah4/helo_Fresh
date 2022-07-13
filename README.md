This is the readme file on how to run code.


Please import all neccessary libararies and API keys

To run the script you will need:

    1. Input file similar to the one provided by HelloFresh for test called Boxes.csv
    2. Input file provided by HelloFresh for test called Temperature_bands.csv
    3. Output filename in the format "<filename>.csv"

Command to run the script:
    1. Using python3;
        The command to run the script will be: "python3 main.py Boxes.csv Temperature_bands.csv Output_data.csv"
        
    Note: i. Substitute the input file "Boxes.csv" with your input file
          ii. The following table properties of the file must be the same as "Boxes.csv":
                a. number of columns
                b. csv column header
                c. index locations of csv clumns and fields

    
    2. To execute the tests:
        python3 test.py box_test_sample1.csv Temperature_bands.csv output1.csv
        python3 test.py box_test_sample2.csv Temperature_bands.csv output2.csv
