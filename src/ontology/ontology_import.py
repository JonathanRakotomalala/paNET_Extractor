import owlready2


class Ontology:
    
    def getting_ontology():

        """ get the ontology from local or from internet"""
        ontology = owlready2. get_ontology("https://data.bioontology.org/ontologies/PANET/submissions/26/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb")
        ontology.load()
        classes=ontology.classes()
        myontology=[]
        
        for i in classes:
            myontology.append({"label":''.join(i.label),"altLabel":i.altLabel,"subClassOf":Ontology.extract_subclass_of(i),"definition1":' '.join(i.IAO_0000115),"definition2":''.join(i.IAO_0000119)})
        return myontology

    def extract_subclass_of(a_class):
        """extract the name and label of the classes from which a_class inherits
        
        Args : 
            a_class: an ontology class
        
        Returns :
            dictionnary containing the classes from which a_class inherit
        
        """
        superclass = a_class.is_a
        output = {}
        for i in superclass:
            output[i.name]=' '.join(i.label)
        return output