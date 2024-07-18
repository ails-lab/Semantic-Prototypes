import os
import os.path as osp
import cv2
import matplotlib.pyplot as plt


class CUB:
        
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.load_data()
        
        
    def load_data(self):
        
        # =========================
        # IMAGES AND CLASS LABELS:
        # =========================
        with open(osp.join(self.dataset_path, "images.txt"), "r") as handle:
            self.image_id_to_image_name = {int (line.strip().split(" ")[0]): line.strip().split(" ")[1] for line  in handle.readlines()}
        
        with open(osp.join(self.dataset_path, "train_test_split.txt"), "r") as handle:
            self.image_id_to_train_label = {int(line.strip().split(" ")[0]): int(line.strip().split(" ")[1]) for line in handle.readlines()}
        
        with open(osp.join(self.dataset_path, "classes.txt"), "r") as handle:
            self.class_id_to_class_name = {int(line.strip().split(" ")[0]): line.strip().split(" ")[1] for line in handle.readlines()}
        
        with open(osp.join(self.dataset_path, "image_class_labels.txt"), "r") as handle:
            self.image_id_to_class_id = {int(line.strip().split(" ")[0]): int(line.strip().split(" ")[1]) for line in handle.readlines()}
        
        
        # =========================
        # PART LOCATIONS:
        # =========================
        
        with open(osp.join(self.dataset_path, "parts/parts.txt"), "r") as handle:
            self.part_id_to_part_name = {int(line.strip().split(" ")[0]): " ".join(line.strip().split(" ")[1:]) for line in handle.readlines()}
        
        self.image_id_to_parts = {}
        with open(osp.join(self.dataset_path, "parts/part_locs.txt"), "r") as handle:
            for line in handle.readlines():
                image_id, part_id, _, _, visible = line.strip().split(" ")
                if int(visible) == 0:
                    continue
                
                part_name = self.part_id_to_part_name[int(part_id)]
                if int (image_id) in self.image_id_to_parts:
                    self.image_id_to_parts[int(image_id)].append(part_name)
                else:
                    self.image_id_to_parts[int(image_id)] = [part_name]

        # =========================
        # ATTRIBUTE LABELS:
        # =========================
        with open(osp.join(self.dataset_path, "attributes/attributes.txt"), "r") as handle:
            self.attribute_id_to_attribute_name = {int(line.strip().split(" ")[0]): line.strip().split(" ")[1] for line in handle.readlines()}
        
        with open(osp.join(self.dataset_path, "attributes/certainties.txt"), "r") as handle:
            self.certainty_id_to_certainty_name = {int(line.strip().split(" ")[0]): line.strip()[2:] for line in handle.readlines()}
        
        self.class_attribute_labels = {}
        with open(osp.join(self.dataset_path, "attributes/class_attribute_labels_continuous.txt"), "r") as handle:
            for cl, row in enumerate(handle.readlines()):
                importance= {self.attribute_id_to_attribute_name[i+1]:float(l) for i, l in enumerate(row.split(" ")) if float(l) > 0}
                self.class_attribute_labels[cl + 1] = {k: v for k, v in sorted(importance.items(), key=lambda item: abs(item[1]), reverse = True)}
        
        self.image_id_to_annotations = {}
        with open(osp.join(self.dataset_path, "attributes/image_attribute_labels.txt"), "r") as handle:
            for line in handle.readlines():
                try:
                    image_id, attribute_id, is_present, certainty_id, time =  line.strip().split(" ")
                except Exception as e:
                    continue
                
                if int(is_present) == 0:
                    continue 
                certainty_name = self.certainty_id_to_certainty_name[int(certainty_id)]
                attribute_name = self.attribute_id_to_attribute_name[int(attribute_id)]
                
                # if certainty_name not in ["probably", "definitely"]:
                #     continue

                # if float (time) < 10:
                #     continue
                
                if int (image_id) in self.image_id_to_annotations:
                    self.image_id_to_annotations[int (image_id)].append(attribute_name)
                else:
                    self.image_id_to_annotations[int (image_id)] = [attribute_name] 
                    
    def print_annotations(self, image_id):
        print (self.image_id_to_annotations[image_id])
        
    def print_parts(self, image_id):
        print (self.image_id_to_parts[image_id])
        
    def print_sample(self, image_id, only_image = False):
        image_name = self.image_id_to_image_name[image_id]
        image_path = osp.join(self.dataset_path, "images", image_name)
        image = cv2.imread(image_path)
        
        if not only_image:
            self.print_parts(image_id)
            self.print_annotations(image_id)
        plt.imshow(image)