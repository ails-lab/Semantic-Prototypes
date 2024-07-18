import os
import json 
import sys
from cece.xDataset import *


### define functions ####
def obj_distance (obj1, obj2):
    lca = obj1.intersection(obj2)
    diffs = len(obj1 - lca) + len(obj2 - lca)
    return diffs

def addition_cost (obj):
    return len(obj)

def removal_cost (obj):
    return len(obj)



def distance_between_samples(objects1, objects2, return_edits = False, verbose = True):
    cost = 0
    edits = {"Added": [], "Removed": [], "Transformed": []}
    objects1 = {i: c for i, c in enumerate (q1.concepts)} # give to each object of q1 a unique id 
    objects2 = {i + len(objects1): c for i, c in enumerate (q2.concepts)} # give to each object of q2 a unique id

    # which concepts are common between the 2 instances
    same_concepts = {}
    for i, c1 in objects1.items():
        for j, c2 in objects2.items():
            if obj_distance(c1, c2) == 0 and j not in same_concepts.values(): # if the objects are the same and this id is not already in the match, ie if the object has not already been matched with other object
                same_concepts[i] = j
                break # stop searching because maybe the same object exists 2 times in the instance e.g. 2 persons or 2 times the same word

    
    if verbose:
        print (f"Remain the same: {same_concepts}")
    
    # the match items must be removed from the list of items
    for i, j in same_concepts.items():
        if verbose:
            print (f"Remains the same: {objects1[i]}")
        objects1.pop(i, None) # remove this object from the list of items of q1
        objects2.pop(j, None) # remove this object from the list of items of w2

        
    combined = set()
    for obj1_id in objects1:
        min_dist = 10e6
        min_match = None
        for obj2_id in objects2:
            obj1 = objects1[obj1_id]
            obj2 = objects2[obj2_id]
            dist = obj_distance(obj1, obj2)
            if dist < min_dist:
                min_dist = dist
                min_match = obj2_id
                
        if min_dist == 10e6:
            if verbose:
                print (f"Removed: {obj1}")
            cost += 500
            edits["Removed"].append(obj1)
        else:
            cost += min_dist
            combined.add((obj1_id, min_match))
            objects2.pop(min_match, None)
            
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
    
### find prototypes ####

dataset_path, label = sys.argv[1], int (sys.argv[2])

with open (dataset_path, "r") as handle:
    scenes = json.load(handle)
   
    

queries = []
labels = []
urls = []
for scene in scenes["scenes"]:
    query = [set(["Image"])]
    for obj in scene["objects"]:
        query.append(set([obj["shape"].capitalize(),
                         obj["color"].capitalize(),
                         obj["material"].capitalize(), 
                         obj["size"].capitalize(),
                         "Object"]))
    q = Query(np.array(query))
    queries.append(q)
    labels.append (scene["class_id"])
    urls.append (scene["image_filename"])
    
    
# define the rules for clevr-hans
rules = {
    0: [
    set(["Image"]), set(["Large", "Cube"]), set(["Large", "Cylinder"]),
],
    1: [
    set(["Image"]), set(["Small", "Metal", "Cube"]), set(["Small", "Sphere"]),
],
    2: [
    set(["Image"]), set(["Large", "Blue", "Sphere"]), set(["Large", "Yellow", "Sphere"]),
]
}


q1 = rules[label]
q1 = Query(np.array(q1))

indexes = {0: [], 1: [], 2: []}
for i in range (len(queries)):
    l = labels[i]
    indexes[l].append(i)


pairs = []
d = {}
for idx in indexes[label]:
    q2 = queries[idx]
    label = labels[idx]

    assert label == label
    c, e = distance_between_samples(q1.concepts, q2.concepts, True, False)
    d[idx] = c

d = [[k, v] for k, v in sorted(d.items(), key=lambda item: item[1])]    
    
    
image_id, distance = d[0]
q2 = queries[idx]

print (f"The closest prototype is the image: {urls[image_id]}")    
    