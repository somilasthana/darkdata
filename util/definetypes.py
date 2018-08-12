class DefineTypes(object):
    
    def __init__(self, dataframe):
        self.df_ = dataframe
        g = self.df_.columns.to_series().groupby(self.df_.dtypes).groups
        self.type_info = {k.name: v.values.tolist() for k, v in g.items()}
        self.type_map = {}
        
    def process_(self):
        for type_name in type_info:
            for column_name in type_info[type_name]:
                self.type_map.setdefault(column_name, type_name)
                
    def correction(self, correct_value_list):
        # inform of (column_name, column_type)
        for column_name, column_type in correct_value_list:
            if column_name in self.type_map:
                self.type_map[column_name] = column_type
            else:
                print("Column Name %s doesnt exist in the system", column_name)
                
    def date_column(self):
        return self.type_info['datetime64[ns]']
    
    def categorical_column(self):
        return self.type_info['object']
