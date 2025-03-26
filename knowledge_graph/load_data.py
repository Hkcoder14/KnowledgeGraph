from neo4j import GraphDatabase
import json

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = ""

#connect to DB
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

def create_entity(tx, entity_text, entity_label):
    query = "MERGE (e:Entity {name: $name, label: $label})"
    tx.run(query, name = entity_text, label = entity_label)

def create_relationships(tx, entity1, relation, entity2):
    query = f"""
    MATCH (e1:Entity {{name: $entity1}})
    MATCH (e2:Entity {{name: $entity2}})
    MERGE (e1)-[:`{relation}`]->(e2)
    """
    tx.run(query, entity1=entity1, entity2=entity2)

def load_data():
    
    with driver.session() as session:
        #loading entities
        with open('data/entities.json', "r") as f:
            entities = json.load(f)
            for entity in entities:
                session.execute_write(create_entity, entity["text"], entity["label"])
            print(f" Loaded {len(entities)} entities into Neo4j.")

        with open("data/relations.json", "r") as f:
            relations = json.load(f)
            for relation in relations:
                session.execute_write(create_relationships, relation["Entity1"], relation["Relation"], relation["Entity2"])
            print(f" Loaded {len(relations)} relations into Neo4j.")

if __name__ == "__main__":
    load_data()
    driver.close()