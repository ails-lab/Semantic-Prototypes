from tqdm.notebook import tqdm
import re
from plotnine import *
import pandas as pd
from matplotlib.pyplot import figure

sorted_colors = ['black',
                 'blue',
                 'brown',
                 'grey',
                 'purple',
                 'pink',
                 'iridescent',
                 'multi-colored',
                 'red',
                 'rufous',
                 'orange',
                 'buff',
                 'yellow',
                 'green',
                 'olive',
                 'white',
]

sorted_lengths = ['shorter_than_head', 'about_the_same_as_head', 'longer_than_head']
size_sorted = ['very_small_(3_-_5_in)', 'small_(5_-_9_in)', 'medium_(9_-_16_in)', 'large_(16_-_32_in)', 'very_large_(32_-_72_in)']
belly_pattern_sorted = ['solid', 'spotted', 'striped', "multi-colored"]
bill_pattern_sorted = ['shorter_than_head', 'about_the_same_as_head', 'longer_than_head'] 


class SetOfSets:

    def __init__(self, sets=[]):
        set_of_sets = []
        for s1 in sets:
            if not any(s2 > s1 for s2 in sets):
                set_of_sets.append(s1)
        self.sets = frozenset(frozenset(s) for s in set_of_sets)

    def __le__(self, other):
        return all(any(s1 <= s2 for s2 in other.sets) for s1 in self.sets)

    def __hash__(self):
        return hash(self.sets)

    def __and__(self, other):
        return SetOfSets(sets=[s1 & s2 for s1, s2 in product(self.sets, other.sets)])

    def __str__(self):
        return str(self.sets)
        
    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.sets)


def get_concept_distance(concept1, concept2):
    
    if concept1 == concept2:
        return 0 
    
    part1, type1 = concept1.split("::")
    part2, type2 = concept2.split("::")
    
    if part1 != part2:
        return 10e6
    else:
        if "color" in part1:
            return (abs(sorted_colors.index(type1) - sorted_colors.index(type2)) * 4)
        elif "shape" in part1:
            type1 = set(re.split(', |_|-|!', type1)) - set(["like", "tail", "wings"])
            type2 = set(re.split(', |_|-|!', type2)) - set(["like", "tail", "wings"])
            inter = type1.intersection(type2)
            return max(50 - len(inter) * 10, 0)
        elif "length" in part1:
            return abs(sorted_lengths.index(type1) - sorted_lengths.index(type2)) * 40
        elif "size" in part1:
            return abs(size_sorted.index(type1) - size_sorted.index(type2)) * 40
        elif part1 in ["has_belly_pattern", "has_wing_pattern", "has_tail_pattern", "has_breast_pattern", "has_back_pattern"]:
            return abs(belly_pattern_sorted.index(type1) - belly_pattern_sorted.index(type2)) * 35
        elif part1 == "has_bill_length":
            return abs(bill_pattern_sorted.index(type1) - bill_pattern_sorted.index(type2)) * 35
        elif part1 == "has_head_pattern":
            return 50

        
def distance_between_samples(objects1, objects2, return_edits = False, verbose = True):
    cost = 0
    edits = {"Added": [], "Removed": [], "Transformed": []}
    same_concepts = objects1.intersection(objects2)
    
    if verbose:
        print (f"Remain the same: {same_concepts}")
    
    objects1 = objects1 - same_concepts
    objects2 = objects2 - same_concepts
    combined = set()
    for obj1 in objects1:
        min_dist = 10e6
        min_match = None
        for obj2 in objects2:
            dist = get_concept_distance(obj1, obj2)
            if dist < min_dist:
                min_dist = dist
                min_match = obj2
                
        if min_dist == 10e6:
            if verbose:
                print (f"Removed: {obj1}")
            cost += 500
            edits["Removed"].append(obj1)
        else:
            cost += min_dist
            combined.add((obj1, min_match))
            objects2.remove(min_match)
            
    if verbose:
        print (f"Transformed: {combined}")
    edits["Transformed"] += list(combined)
    
    for obj2 in objects2:
        cost += 500
        
    if verbose:
        print (f"Added: {objects2}")
    
    edits["Removed"] += objects2
    
    if return_edits:
        return cost, edits
    else:
        return cost
    
    
class GlobalEdits:
    
    def __init__(self):
        self.global_edits = {}
        
        
    def update_dict(self, concept, value):
        if concept not in self.global_edits:
            self.global_edits[concept] = value
        else:
            self.global_edits[concept] += value
        
    def push(self, edits):
        for concept in edits["Added"]:
            self.update_dict(concept, 1)
                
        for concept in edits["Removed"]:
            self.update_dict(concept, -1)
                
        for source, target in edits["Transformed"]:
            self.update_dict(source, -1)
            self.update_dict(target, 1)
        
        
    def plot(self, title = "", length = 30):
        self.global_concepts = [[k, v] for k, v in sorted(self.global_edits.items(), key=lambda item: abs(item[1]), reverse = True)][:length]
        df = pd.DataFrame({"Objects":[a[0] for a in self.global_concepts], "y": [a[1] for a in self.global_concepts]})
        return (ggplot(aes(x="Objects", weight="y",), df) +
         geom_bar(fill="#619CFF") + 
         ylab("") + xlab("") + 
         scale_x_discrete(limits=df['Objects'].tolist()) +
         theme_minimal() +
         theme(axis_text_x=element_text(rotation=90, hjust=1)) + 
         labs(title = title)) 
    