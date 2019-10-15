# Roll No.= 17CS30026
# Praagy Rastogi
# Assignment 1
# Decision Tree

import csv
import numpy 


# Calculate entropy on splitting according to a particular attribute
def info_gain_attribute(data, idx):

    total_entropy= calculate_entropy(data[-1])
    attribute_entropy= 0
    obj,count= numpy.unique(data[idx], return_counts=True)
    
    for i in range(len(obj)):
        bool_=[]
        for p in range(len(data[len(data)-1])):
            if obj[i]==data[idx][p]:
                bool_.append(data[len(data)-1][p])

        attribute_entropy+= calculate_entropy(bool_)*((1.0*count[i])/numpy.sum(count))

    info_gain= total_entropy - attribute_entropy
    return info_gain

# Calculate entropy of a single attribute
def calculate_entropy(bool_):

    obj,count= numpy.unique(bool_, return_counts=True)
    entropy=0
    for i in range(len(obj)):
        fraction=1.0*count[i]/numpy.sum(count)
        entropy+= -fraction * numpy.log2(fraction)

    return entropy

#Recursive Function builds tree as type dict(string:dict)  
def build_tree(category, data, data_original, attributes, done, parent_node=None):

    if len(numpy.unique(data[len(data)-1])) <= 1: # entropy is 0
        return numpy.unique(data[len(data)-1])[0] # either yes or no
    elif len(data)== 0:
        i=numpy.argmax(numpy.unique(data_original[len(data_original)-1], return_counts=True)[1])
        return numpy.unique(data_original[len(data_original)-1])[i]

    elif all(i== 1 for i in done):
        return parent_node
    else:
        i=numpy.argmax(numpy.unique(data[len(data)-1], return_counts=True)[1]) #majority value index
        parent_node= numpy.unique(data[len(data)-1])[i] # majority value

        info_gain= []
        for i in range(len(attributes)):
            if done[i]==1:
                info_gain.append('-inf')
            else:
                info_gain.append(info_gain_attribute(data, i))

        max_gain_attribute= numpy.argmax(info_gain) # attribute with max information gain
        done[max_gain_attribute]= 1

        tree= {category[max_gain_attribute]:{}} # split the max_gain_attribute

        for c in numpy.unique(data[max_gain_attribute]):

            sub_data= [[] for _ in range(len(data))]
            for p in range(len(data[max_gain_attribute])):

                if data[max_gain_attribute][p]==c:
                    for i in range(len(data)):
                        sub_data[i].append(data[i][p])
            subtree= build_tree(category, sub_data, data_original, attributes, numpy.copy(done), parent_node)
            tree[category[max_gain_attribute]][c]= subtree
        
        return tree

def print_tree(tree, spaces=0):

    sp="   "*spaces
    if type(tree) == dict:
        for key in tree:
            for k in tree[key]:
                print(sp+key+' = '+k+" ->")
                print_tree(tree[key][k], spaces + 1)
        return

    print(sp+tree)
    return

def read_csv(path):

    bool_= []
    attributes= [] 
    category= {}
    first_row=True

    with open(path,'rt') as file:
        data= csv.reader(file)
        for row in data:
            if first_row:
                first_row=False
                attributes= [[] for _ in range(len(row)-1)]
                for i in range(len(row)-1):
                    category.update({i :row[i]})
            else:
                bool_.append(row[len(row)-1])
                for i in range(len(row)-1):
                    attributes[i].append(row[i])
                
    done= numpy.zeros(len(attributes))
    data= attributes[:]
    data.append(bool_)

    return category,data,attributes,done


def main():

    # Read data from csv file
    category,data,attributes,done= read_csv('./data1_19.csv')

    # Build Decision tree recursively by splitting nodes
    tree= build_tree(category,data,data,attributes,done)

    # Show output tree
    print_tree(tree)

if __name__== '__main__':
    main()