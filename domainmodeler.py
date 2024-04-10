import json

from Relationship import Relationship
from UtilityFunctions import get_completion_from_messages

from graphviz import Digraph

class DomainModeler:
    def __init__(self, user_stories):
        self.user_stories = user_stories
        self.role_list = []
        self.role_count = 0
        self.role_class_list = []
        self.role_class_count = 0
        self.non_role_class_list = []
        self.non_role_class_count = 0
        self.class_list = []
        self.class_count = 0
        self.relationships_list = []
        self.relationships_count = 0
    def get_roles(self):

        self.role_list = []
        self.role_count = 0

        prompt = """
    User Story has three parts to it:
    Role: As a <Role>
    Function: I want <Function>
    Benefit: so that <Benefit>

    Identify the distinct roles mentioned in the 'Role' part of all the user stories. Give the output in the following JSON format:

    {
      "roles": [
    	...
      ]
    }
        """
        response = get_completion_from_messages(self.user_stories, prompt)

        roles_json = json.loads(response)
        for role in roles_json['roles']:
            if role is not None:
                self.role_list.append(role)
            self.role_count = self.role_count + 1

        return

    def get_role_classes(self, role_list_to_convert):

        self.role_class_list = []
        self.role_class_count = 0

        if len(role_list_to_convert) == 0:
            return
        elif len(role_list_to_convert) > 0:
            prompt = """
Represent the roles in the following list: """ + f"{str(role_list_to_convert)}" + """ as classes and mention their attributes and behavior (methods/ functions) in the following JSON format:
{
  "classes": [
    {
      "name": 
      "attributes": [
        {
          "name": 
          "type": 
        },
	...
      ],
      "methods": [
        {
          "name": ,
          "parameters": [
            {
              "name": ,
              "type": 
            },
	    ...
          ],
          "returnType": 
        },
        ...
      ]
    },
    ...
  ]
}
        """
            response = get_completion_from_messages(self.user_stories, prompt)
            print("PROMPT")
            print(prompt)

            print("JSON")
            print(response)

            with open("role_classes.json", "w") as f:
                f.write(response)

            classes_json = json.loads(response)
            for cls in classes_json['classes']:
                if cls is not None:
                    self.role_class_list.append(cls["name"])
                self.role_class_count = self.role_class_count + 1
        return

    def get_non_role_classes(self):

        self.non_role_class_list = []
        self.non_role_class_count = 0

        prompt = """
Identify and Represent the classes involved in the user stories other than in the following list: """ + f"{str(self.role_class_list)}" + """ mentioning their attributes and behavior (methods/ functions) in the following JSON format:
{
  "classes": [
    {
      "name": 
      "attributes": [
        {
          "name": 
          "type": 
        },
	...
      ],
      "methods": [
        {
          "name": ,
          "parameters": [
            {
              "name": ,
              "type": 
            },
	    ...
          ],
          "returnType": 
        },
        ...
      ]
    },
    ...
  ]
}
        """
        response = get_completion_from_messages(self.user_stories, prompt)
        print("PROMPT")
        print(prompt)

        print("JSON")
        print(response)

        with open("non_role_classes.json", "w") as f:
            f.write(response)

        classes_json = json.loads(response)
        for cls in classes_json['classes']:
            if cls is not None:
                self.non_role_class_list.append(cls["name"])
            self.non_role_class_count = self.non_role_class_count + 1
        return

    def get_role_classes_json(self, role_list_to_convert):

        prompt = """
Convert the following roles: """ + f"{str(role_list_to_convert)}" + """ into classes. Give the output in the following JSON format:

    {
      "classes": [   
          {
               "name": 
           },
    	...
      ]
    }
Note: The name of each class must strictly follow camel case naming convention.
        """
        response = get_completion_from_messages(self.user_stories, prompt)
        return response

    def get_non_role_classes_json(self):
        prompt = """
Find the classes, other than in the following list: """ + f"{str(self.role_class_list)}" + """ , from the user stories. Give the output in the following JSON format:

    {
      "classes": [   
          {
               "name": 
           },
    	...
      ]
    }
Note: The name of each class must strictly follow camel case naming convention. Only output JSON data with in {}, nothing else.
            """
        response = get_completion_from_messages(self.user_stories, prompt)
        print(response)
        return response

    def read_classes_json(self, classes_json):
        role_classes = []
        role_classes_count = 0
        classes_json = json.loads(classes_json)
        for cls in classes_json['classes']:
            if cls is not None:
                role_classes.append(cls["name"])
                role_classes_count = role_classes_count + 1

        return role_classes_count, role_classes

    def get_relationships_json(self):
        prompt = """
Find relationships  between the following classes:  """ + f"{str(self.class_list)}" + """  involved in the user stories.
 Output the relationships in the following JSON format:
{
  "relationships": [
       {
          "name": ,
          "source": class,
          "target": class
        },
   ...
}
Only output JSON data with in {}, nothing else.
        """
        print(prompt)
        response = get_completion_from_messages(self.user_stories, prompt)
        return response

    def read_relationships_json(self, relationships_json):
        relationships_list = []
        relationships_count = 0
        relationships_json = json.loads(relationships_json)
        for relationship in relationships_json['relationships']:
            if relationship is not None:
                relationship_object = Relationship(relationship["source"], relationship["name"], relationship["target"])
                relationships_list.append(relationship_object)
                relationships_count = relationships_count + 1

        return relationships_count, relationships_list

    def create_domain_model_graph(self):
        gra = Digraph(format="png")
        # gra.format = "png"
        for relationship in self.relationships_list:
            gra.node(relationship.subject, relationship.subject, shape="box")
            gra.node(relationship.object, relationship.object, shape="box")
            gra.edge(relationship.subject, relationship.object, label=relationship.predicate)

        print(gra.source)
        file_name="class_diagram"
        gra.render(file_name, view=True)

        return file_name
