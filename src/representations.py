


class OrdinalBinnerForInts:
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
                 raw_binner_list, variable_names):
        """ 
        Import data from file.  Prioritize frequency table over raw_csv.
        
        Use raw_binner_list to store binner.  None means variable is not 
        preserved in aggregation.  True means variable is not binned.

        Return True if data successfully read, false if not.
        """

        # reason for how I handle file non-existence or read failure:
        # https://mail.python.org/pipermail/python-ideas/2009-May/004900.html

        try:
            with open(frequency_table_csv) as f

                # TODO; read frequency table
        except:
            try:
                with open(frequency_table_csv) as f

            except:
                return False

        return True            


if __name__ == "__main__":


    score_binner = OrdinalBinnerForInts([-1,0,5])
    favorite_count_binner = OrdinalBinnerForInts([0])
    answer_count_binner = OrdinalBinnerForInts([0])
    comment_count_binner = OrdinalBinnerForInts([0,3])


    ds = Dataset(




