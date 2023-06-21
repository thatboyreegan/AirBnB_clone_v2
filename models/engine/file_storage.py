#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    # NB: Better to have two file paths.
    #     One for testing and the other for development so as not to
    #     lose data when testing as it overwrites existing file.
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage or of a
        specific class if given.

        Args:
            cls (class): Class to return all models of it. Defaults to None.
        """

        if cls:
            # Getting class objects without dictionary comprehension.
            # cls_objects = {}
            # for key, value in FileStorage.__objects.items():
            #     if isinstance(value, cls):
            #         cls_objects[key] = value
            # return cls_objects

            return {
                key: value
                for key, value in FileStorage.__objects.items()
                if isinstance(value, cls)
            }
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.__class__.__name__ + "." + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, "w") as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f, indent=4)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, "r") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside.

        Args:
            obj (object): Object to delete. Defaults to None.
        """

        if obj and obj in FileStorage.__objects.values():
            key = f"{obj.__class__.__name__}.{obj.id}"
            del FileStorage.__objects[key]
            self.save()
