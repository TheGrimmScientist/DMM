""" Tested and developed on python 2.7 and numpy 1.8"""

# new or old style classes?
#http://stackoverflow.com/questions/54867/old-style-and-new-style-classes-in-python


class Variable:
    """ A variable is both a name and a cardinality """
    def __init__(self, name, cardinality):
        self.name = name
        self.cardinality = cardinality

import Data


class Component:
    """  """
    def __init__(self,extracted_component):

        self.df = None

    def return_entropy(self):
        pass

class ComponentWithData(Component):
    """ """
    def __init__(self):
        self.test = 5
        self.data = extracted_component # should this be copied?
        self.entropy = None

class Model:
    def __init__(self,variable_list=None):
        #if initing from text string, preserve order as much as possible
        raise Exception("Model class not yet written")


if __name__ == "__main__":

    print "\n ======== Begin ============\n\n"

    ds = Data.Dataset(raw_csv="../../SampleDatasets/StackExchange/CrossValidated_AllPosts_140119.csv",
                 binners=[["Score",Data.OrdinalBinner([-1,0,5]), int ],
                          ["FavoriteCount",Data.OrdinalBinner([0]), int ],
                          ["AnswerCount",Data.OrdinalBinner([0]), int ],
                          ["CommentCount",Data.OrdinalBinner([0,3]), int ],
                          ["Body",Data.TextLengthBinner([0,50,100,300]), str ]])
                          # need to include what type to expect in order to properly clean
                          

    print "N of dataset:", ds.N

    # print "Frequency matrix for full dataset:"
    # print ds.frequency_matrix

    # ds.save_frequency_table("")

    # print ds.probability_matrix


    # print "Some test cases to check aggregation"
    # l = []
    # print l,'\n',ds.extract_component(l),'\n'
    # l = [1,0,3]
    # print l,'\n',ds.extract_component(l),'\n'

    occam3_filename = "test_file.oin"
    print "saving ",occam3_filename,"..."
    ds.save_as_occam3_format(occam3_filename)


    # E0: entropy of a single component

    # E1: entropy of a model with one component.  ==E0?


    print "\n\n ======== End ============\n"

#  Todo:
#    - it may be cleaner to make the binner objects a part of Variable.
#    - it'd be nice to have some automatic binning functions on the front end.

