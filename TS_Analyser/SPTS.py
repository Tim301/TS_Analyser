class SPTS(MPTS):
    def __init__(self,name):
        self.path = ts_folder + name
        self.length = tools.get_length(self.path) # frames