from abc import ABC, abstractmethod
import json
from turtle import width
from typing import Any

from models.product import Product

class BaseRepository(ABC):
    def __init__(self, name: str):
        self.name: str = name
        
    @abstractmethod
    def get(self, id: int | None = None, param="id"):
        with open(f"data/{self.name}.json") as file:
            data = json.load(file)
            if(id == None):
                return data
            else: 
                selected_items = []
                for item in data:
                    if item[param] == int(id):
                        selected_items.append(item)
                print("Selected Items", selected_items)
                if not len(selected_items):
                    return None
                elif len(selected_items) == 1:
                    return selected_items[0]
                else:
                    return selected_items
                
                
    @abstractmethod
    def add(self, data):
        with open(f"data/{self.name}.json", "r+") as file:
            try: 
                contents = json.load(file)
                contents.append(data)
                file.truncate(0)
                file.seek(0)
                data = json.dumps(contents)
                n = file.write(data)
                if not n:
                    raise Exception("Error Occured While adding to the database")
                else:
                    return True
            except Exception as err:
                return err    
            # file.write(data)
            # print(new_data)
    @abstractmethod
    def delete(self, id: str):
        pass
    @abstractmethod
    def update(self, data: Any, id: int):
        print(data)
        try: 
            if id == None or not id:
                raise Exception("Id is required")
            with open(f"data/{self.name}.json", "r+") as file:
                contents = json.load(file)
                updated_contents = []
                item = self.get(int(id))
                if item == None:
                    raise Exception(f"{self.name} Id doesn't exists")
                for content in contents:
                    if content["id"] == id:
                        updated_contents.append(data) 
                    else:
                        updated_contents.append(content)
                file.truncate(0)
                file.seek(0)
                new_data = json.dumps(updated_contents)
                file.write(new_data)
                return data 
        except Exception as err:
            return err
        