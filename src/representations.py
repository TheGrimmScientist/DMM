
import csv
import numpy as np

class OrdinalBinner:
    """
    Automate the binning of ordinal data into categorical data.  Given
    a list of the upper limits of each bin on init, give access to varaible's
    cardinality through get_cardinality(), and provide bin_val() for the 
    binning of a single value of a variable.
    """
    
    def __init__(self, upper_limits):
        self.upper_limits = upper_limits
        
    def get_cardinality(self):
        return len(self.upper_limits)+1
    
    def bin_val(self, value):
        for i,limit in enumerate(self.upper_limits):
            if value <= limit:
                return i
        return i+1



class Dataset:
    """ Stuff """
    def __init__(self, frequency_table_csv=None, raw_csv=None,
                 binners=None, raw_variable_names=None):
        """ 
        Import data from file.  Prioritize frequency_table_csv over raw_csv.
        
        If frequency_table_csv is used:
            Expect a header line holding the variable names.

        If raw_csv is used:  
            if raw_csv includes a header, expect raw_variable_names = None.
                else expect raw_variable_names = <list of varaible names>.
            Parameter binners  

        Use raw_binner_list to store binner.  None means variable is not 
        preserved in aggregation.  True means variable is not binned.

        Return True if data successfully read, false if not.
        """

        # reason for how I handle file non-existence or read failure:
        # https://mail.python.org/pipermail/python-ideas/2009-May/004900.html

        try:
            with open(frequency_table_csv,'r') as f:

                expected_length = len(variable_names)
                # TODO; read frequency table
                raise Exception("Import frequency_table_csv not yet written.")

        except:
            try:
                with open(raw_csv,'r') as f:
                    reader = csv.reader(f)

                    # Compile header
                    if raw_variable_names is None:
                        header = reader.next()
                    else:
                        header = raw_variable_names
                    
                    # This is where I'd compile the cardinality lists for
                    # variables without a binner object if I wanted to allow
                    # it.  Though I'm making users explitily provide binner
                    # objects to make the user define what is expected from a 
                    # dataset.  Otherwise, this method won't be able to handle
                    # any missing values from the first dataset used to
                    # initialize the model.
                    
                    # Initialize frequency matrix
                    card_list = [val[1].get_cardinality() for val in binners]
                    self.frequency_matrix = np.zeros(tuple(card_list),
                                                     dtype='u4')

                    var_pointer = [header.index(val[0]) for val in binners]
                    expected_length = len(header)
                    for l,row in enumerate(reader):
                        
                        if not expected_length == len(row):
                            for i, item in enumerate(row):
                                print "**%d**"%i,item
                            raise Exception("Invalid row length",
                                            "length: %d"%len(row),
                                            "line number: %d"%l)
                        extracted_row = [row[i] for i in var_pointer]
                        cleaned_row = [0 if val == '' else int(val) 
                                       for val in extracted_row]
                        binned_row = [binners[i][1].bin_val(val) for 
                                      i,val in enumerate(cleaned_row)]
                        self.frequency_matrix[tuple(binned_row)] += 1

            except Exception, e:
                raise e

        self.variable_list = None



    def save_frequency_table(filename):
        pass


if __name__ == "__main__":

    print "\n ======== Begin ============\n\n"

    ds = Dataset(raw_csv="../../SampleDatasets/StackOverflowSample.csv",
                 binners=[["Score",OrdinalBinner([-1,0,5]) ],
                          ["FavoriteCount",OrdinalBinner([0]) ],
                          ["AnswerCount",OrdinalBinner([0]) ],
                          ["CommentCount",OrdinalBinner([0,3]) ]])

    print ds.frequency_matrix

    ds.save_frequency_table()


    print "\n\n ======== End ============\n"

