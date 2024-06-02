import lxml.etree as ET
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, DC, DCTERMS, XSD, OWL

# Define namespaces
EX = Namespace("http://example.org/")
TEI = Namespace("http://www.tei-c.org/ns/1.0")
DBO = Namespace("http://dbpedia.org/ontology/")
GEO = Namespace("http://www.geonames.org/ontology#")

# Create a new graph
g = Graph()
g.bind("foaf", FOAF)
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)
g.bind("dbo", DBO)
g.bind("owl", OWL)
g.bind("geo", GEO)

# Parse the TEI XML file
tree = ET.parse('Reagan_speech.xml')
root = tree.getroot()

# Helper function to create URIs
def create_uri(base, name):
    return URIRef(f"{base}{name.replace(' ', '_')}")
'''
# Helper function to create URIs
def create_uri(base, name):
    return URIRef(f"{base}{name}")
'''
    
# Transform persons
for pers_name in root.findall('.//{http://www.tei-c.org/ns/1.0}persName'):
    uri = create_uri(EX, pers_name.get('ref').strip('#'))
    g.add((uri, RDF.type, FOAF.Person))
    if pers_name.text:
        g.add((uri, FOAF.name, Literal(pers_name.text.strip(), datatype=XSD.string)))
    if 'role' in pers_name.attrib:
        g.add((uri, DBO.role, Literal(pers_name.get('role'), datatype=XSD.string)))

# Transform organizations
for org_name in root.findall('.//{http://www.tei-c.org/ns/1.0}orgName'):
    uri = create_uri(EX, org_name.get('ref').strip('#'))
    g.add((uri, RDF.type, FOAF.Organization))
    if org_name.text:
        g.add((uri, FOAF.name, Literal(org_name.text.strip(), datatype=XSD.string)))

# Transform places
for place_name in root.findall('.//{http://www.tei-c.org/ns/1.0}placeName'):
    uri = create_uri(EX, place_name.get('ref').strip('#'))
    g.add((uri, RDF.type, GEO.Feature))
    if place_name.text:
        g.add((uri, FOAF.name, Literal(place_name.text.strip(), datatype=XSD.string)))

# Transform dates
for date in root.findall('.//{http://www.tei-c.org/ns/1.0}date'):
    event_uri = create_uri(EX, "event" + date.get('when', date.get('notBefore', date.get('from', ''))))
    if 'when' in date.attrib:
        g.add((event_uri, DCTERMS.date, Literal(date.get('when'), datatype=XSD.date)))
    elif 'from' in date.attrib and 'to' in date.attrib:
        g.add((event_uri, DCTERMS.date, Literal(f"{date.get('from')}/{date.get('to')}", datatype=XSD.string)))


# Transform objects
for obj in root.findall('.//{http://www.tei-c.org/ns/1.0}object'):
    obj_uri = create_uri(EX, obj.text.strip())
    g.add((obj_uri, RDF.type, DBO.Object))

# Transform terms
for term in root.findall('.//{http://www.tei-c.org/ns/1.0}term'):
    term_uri = create_uri(EX, term.text.strip())
    g.add((term_uri, RDF.type, DBO.Term))

# Save the RDF graph to a file
g.serialize(destination='Reagan_speech.rdf', format='xml')
