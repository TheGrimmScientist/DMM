""" Tested and developed on python 2.7 and numpy 1.8"""

# new or old style classes?
#http://stackoverflow.com/questions/54867/old-style-and-new-style-classes-in-python

import numpy as np
import Data

def calculate_entropy_of_ndarray(probability_matrix):
    calc_cell_entropies = np.vectorize(lambda x: -x*np.log2(x) if x > 0 else 0.)
    return np.sum(calc_cell_entropies(probability_matrix))


class Variable:
    """ A variable is both a name and a cardinality """
    def __init__(self, name, cardinality, abbreviation=None):
        self.name = name
        self.cardinality = cardinality
        self.abbreviation = abbreviation

    def __str__(self):
        """ 
        Use the abbreviation if givne.  Otherwise use the 
        raw variable name.
        """
        return self.name if self.abbreviation is None else self.abbreviation

class Component:
    """  """
    def __init__(self,list_of_vars):

        self.list_of_vars = list_of_vars
        self.df = None

    def return_df(self):
        """ 
        Degrees of freedom equals the number of cells in the component's
        probability matrix minus 1.  #TODO: add citation.
        """
        if self.df is None:
            self.df = reduce(lambda a,b:a*b,[var.cardinality for var in self.list_of_vars],1) - 1
        return self.df

    def __str__(self):
        """ Join each str(Variable) by commas. """
        return ','.join([str(var) for var in self.list_of_vars])

class ComponentWithData(Component):
    """ """
    def __init__(self,list_of_vars,dataset):
        #TODO: Do I need to re-specify this, or does inheritance take care of it?
        self.list_of_vars = list_of_vars
        self.df = None

        # dataset is expecting variable names, not variable objects
        self.data = dataset.extract_component(
                [var.name for var in self.list_of_vars])

        self.entropy = None


    def return_entropy(self):
        """
        Return entropy of this component.
        Calculate entropy the first time this function is called.
        """
        if self.entropy is None:
            var_names = [var.name for var in self.list_of_vars]
            probability_matrix = ds.extract_component(var_names)
            self.entropy = calculate_entropy_of_ndarray(probability_matrix)
        return self.entropy

class Model:
    def __init__(self,variable_list=None):
        #if initing from text string, preserve order as much as possible
        raise Exception("Model class not yet written")


if __name__ == "__main__":

    print "\n ======== Begin ============\n\n"


    ## Dataset:

    #TODO: make binning object a part of Variable
    #TODO: Let the user specify a variable name to read from
    #and also a different variable name to refernce in Varaible.
    ds = Data.Dataset(raw_csv="../../SampleDatasets/StackExchange/CrossValidated_AllPosts_140119.csv",
                 binners=[["Score",Data.OrdinalBinner([-1,0,5]), int ],
                          ["FavoriteCount",Data.OrdinalBinner([0]), int ],
                          ["AnswerCount",Data.OrdinalBinner([0]), int ],
                          ["CommentCount",Data.OrdinalBinner([0,3]), int ],
                          ["Body",Data.TextLengthBinner([0,50,100,300]), str ]])
                          # need to include what type to expect in order to properly clean
                          

    print "N of dataset:", ds.N, "\n"


    #### Test Occam3 print function
    occam3_filename = "test_file.oin"
    print "saving ",occam3_filename,"..."
    ds.save_as_occam3_format(occam3_filename)


    ## Variable:
    score = Variable(name="Score", cardinality=4, abbreviation='S')
    favorite_count = Variable(name="FavoriteCount", cardinality=2, abbreviation='F')
    answer_count = Variable(name="AnswerCount", cardinality=2, abbreviation='AC')
    comment_count = Variable(name="CommentCount", cardinality=3)
    body_length = Variable(name="Body", cardinality=5, abbreviation='B')

    variable_list = [score, favorite_count, answer_count, comment_count, body_length]
    print "\nVariable List: ", ','.join(map(str,variable_list))


    ## Component:
    print "\nComponents:"
    c1 = Component([score, favorite_count, body_length])
    c2 = Component([])
    c3 = Component([score,favorite_count,answer_count,comment_count,body_length])

    #### Test component print and df functions.

    print "component: ", c1, ". degrees of freedom: ", c1.return_df()
    print "component: ", c2, ". degrees of freedom: ", c2.return_df()
    print "component: ", c3, ". degrees of freedom: ", c3.return_df()


    ## ComponentWithData:
    print "\nComponentWithDatas:"

    cwd1 = ComponentWithData([score, favorite_count, body_length],ds)
    cwd2 = ComponentWithData([],ds)
    cwd3 = ComponentWithData([score,favorite_count,answer_count,comment_count,body_length],ds)

    print "component: ",cwd1,", df: ",cwd1.return_df(),". entropy: ",cwd1.return_entropy()
    print "component: ",cwd2,", df: ",cwd2.return_df(),". entropy: ",cwd2.return_entropy()
    print "component: ",cwd3,", df: ",cwd3.return_df(),". entropy: ",cwd3.return_entropy()



    # E0: entropy of a single component

    # E1: entropy of a model with one component.  ==E0?


    print "\n\n ======== End ============\n"

#  Todo:
#    - it may be cleaner to make the binner objects a part of Variable.
#    - it'd be nice to have some automatic binning functions on the front end.
