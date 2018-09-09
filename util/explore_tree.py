from pandas_summary import DataFrameSummary
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn import metrics
import numpy as np

class Explore_Tree:
    
    def __init__(self, X_train, y_train, m):
        
        self.X_train = X_train
        self.y_train = y_train
        self.m = m
        
    def get_tree_attr(self):
        
        self.n_nodes_ = [t.tree_.node_count for t in self.m.estimators_]
        self.children_left_ = [t.tree_.children_left for t in self.m.estimators_]
        self.children_right_ = [t.tree_.children_right for t in self.m.estimators_]
        self.feature_ = [t.tree_.feature for t in self.m.estimators_]
        self.threshold_ = [t.tree_.threshold for t in self.m.estimators_]
        self.tree_object_ = [t.tree_ for t in self.m.estimators_]
        
    def get_tree_rules(self):
        
        
        rule_map = {}
        self.get_tree_attr()
        
        def explore_tree(estimator, n_nodes, children_left,children_right, feature,threshold,
                suffix='', print_tree= False, sample_id=0, feature_names=None, tree_instance = None):

            if not feature_names:
                feature_names = feature

    
            #assert len(feature_names) == X.shape[1], "The feature names do not match the number of features."
            # The tree structure can be traversed to compute various properties such
            # as the depth of each node and whether or not it is a leaf.
            node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
            node_value = np.zeros(shape=n_nodes, dtype=np.int64)
            is_leaves = np.zeros(shape=n_nodes, dtype=bool)

            stack = [(0, -1)]  # seed is the root node id and its parent depth
    
            store_stack = [rule_map]
            while len(stack) > 0:
                node_id, parent_depth = stack.pop()
                r_mp = store_stack.pop()
                node_depth[node_id] = parent_depth + 1
                r_mp.setdefault(node_id,{})
                r_mp[node_id].setdefault("threshold", threshold[node_id])
                r_mp[node_id].setdefault("Feature", feature_names[feature[node_id]])

                # If we have a test node
                if (children_left[node_id] != children_right[node_id]):
                    store_stack.append(r_mp[node_id])
                    stack.append((children_left[node_id], parent_depth + 1))
            
                    store_stack.append(r_mp[node_id])
                    stack.append((children_right[node_id], parent_depth + 1))
                else:
                    is_leaves[node_id] = True
                    if tree_instance:
                        node_value[node_id] = tree_instance.value[node_id]#tree_object_[tree_no].value[node_id]
                        r_mp[node_id]={"value": node_value[node_id]}

                print("The binary tree structure has %s nodes" % n_nodes)
                r_mp = rule_map
                if print_tree:
                    print("Tree structure: \n")
                    for i in range(n_nodes):
            
                        if is_leaves[i]:
                            print("%s (leaf node=%s) %f" % (node_depth[i] * "\t", i, node_value[i]))
                        else:

                            print("%snode=%s: go to node %s if %s <= %s else to "
                                "node %s." % (node_depth[i] * "\t", i,
                                children_left[i],
                                feature_names[feature[i]],
                                threshold[i],
                                children_right[i],
                           ))
                        print("\n")
            print()
        
        for i,e in enumerate(self.m.estimators_):

            print("Tree %d\n"%i)
            explore_tree(self.m.estimators_[i], self.n_nodes_[i], self.children_left_[i], 
                         self.children_right_[i], self.feature_[i], self.threshold_[i], suffix=i, print_tree=True ,
                         sample_id=1, feature_names=["%s"%ic for ic in self.X_train.columns], tree_instance= self.tree_object_[i])
            print('\n'*2)
            break
        return rule_map
