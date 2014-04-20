""" Tested and developed on python 2.7 and numpy 1.8"""

import numpy as np
import Data
# from sets import Set,ImmutableSet

def calculate_entropy_of_ndarray(probability_matrix):
    calc_cell_entropies = np.vectorize(lambda x: -x*np.log2(x) if x > 0 else 0.)
    return np.sum(calc_cell_entropies(probability_matrix))


class Variable(object):
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

class Component(object):
    """  """
    def __init__(self,var_list):

        self.var_list = var_list
        self.df = None

    def return_df(self):
        """ 
        Degrees of freedom equals the number of cells in the component's
        probability matrix minus 1.  #TODO: add citation.
        """
        if self.df is None:
            self.df = reduce(lambda a,b:a*b,[var.cardinality for var in self.var_list],1) - 1
        return self.df

    def __str__(self):
        """ Join each str(Variable) by commas. """
        return ','.join([str(var) for var in self.var_list])

class ComponentWithData(Component):
    """ """
    def __init__(self,var_list,dataset):
        Component.__init__(self,var_list)

        # dataset is expecting variable names, not variable objects
        self.data = dataset.extract_component(
                [var.name for var in self.var_list])

        self.entropy = None


    def return_entropy(self):
        """
        Return entropy of this component.
        Calculate entropy the first time this function is called.
        """
        if self.entropy is None:
            var_names = [var.name for var in self.var_list]
            probability_matrix = ds.extract_component(var_names)
            self.entropy = calculate_entropy_of_ndarray(probability_matrix)
        return self.entropy

class Model(object):
    def __init__(self,component_list=None):
        self.component_list = component_list

        raise Exception("Model class not yet written")

        self.df = None
        self.loopy = None

    def return_df(self):
        if self.df is None:
            raise Exception("df calculation goes here.")
        return self.df

    def return_loopiness(self):
        if self.loopy is None:
            raise Exception("loopiness function goes here.")
        return self.loopy

    def __str__(self):
        """ Join each 'Str(Component)'s with colons. """
        return ':'.join([str(k) for k in self.component_list])

class ModelWithData(Model):
    def __init__(self, component_list, dataset):

        # Extract unique list of variables from components along with a way
        # to access the var's cardinality.
        var_ref = {}
        for k in component_list:
            for var in k.var_list:
                var_ref[var.name] = var
        # Save those variables in the order they appear in the dataset.
        var_list = []
        card_list = []
        for var_name in dataset.variable_names:
            if var_name in var_ref:
                var_list.append(var_ref[var_name].name)
                card_list.append(var_ref[var_name].cardinality)
        #the whole point of the above is to build the following two tuples:
        self.var_names = tuple(var_list)
        self.var_cards = tuple(card_list)

        # TODO:extract component p tables (like in ComponentWithData):

        # initialize q:
        q = np.zeros(self.var_cards) #init to zeros?

        # TODO: IPF goes here.

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
    answer_count = Variable(name="AnswerCount", cardinality=2, abbreviation='A')
    comment_count = Variable(name="CommentCount", cardinality=3, abbreviation='C')
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

    print "\nModels:"


    print "\nModelWithDatas:"

    print "\n\n ======== End ============\n"


    # E0: entropy of a single component

    # E1: entropy of a model with one component.  ==E0?



#  Todo:
#    - it may be cleaner to make the binner objects a part of Variable.
#    - it'd be nice to have some automatic binning functions on the front end.
