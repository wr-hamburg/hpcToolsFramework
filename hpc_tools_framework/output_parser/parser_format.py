class Parser_format():
    """Class to give instructions to the parser on where to bre4ak lines and what latex elements to add.
    """
    def __init__(self, format):
        self.format = format
        """Dict[int, List]
        Map the line number on a list of Str indices on hwere to break the lines and add the lines to the file.
        Alternativly you can specify line nubers where you want certain latex elements. 
        In order to prevent overwrites, Latex elements in line x are specified as x.5 so, the text in line x can still be formated.  
        Use a list with two elements in the form \ELEMENT_1\{ELEMENT_2\} to specify structure elemnts. 
        """
