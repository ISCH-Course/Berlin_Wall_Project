import csv
import rdflib
from rdflib.namespace import XSD, RDF
from rdflib import Namespace, URIRef, Literal
import requests

fabio = Namespace("http://purl.org/spar/fabio/")
mo = Namespace("http://purl.org/ontology/mo/")
fo = Namespace("https://semantics.id/ns/example/film/")
schema = Namespace("https://schema.org/")
dcterms = Namespace("https://www.dublincore.org/specifications/dublin-core/dcmi-terms/")
rico = Namespace("https://www.ica.org/standards/RiC/ontology/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
rdfs = Namespace("https://www.w3.org/2000/01/rdf-schema#")
lode = Namespace("https://linkedevents.org/ontology/")

path = "<https://w3id.org/BerlinWallProject/"
literals = ["crm:P45 consists of",
            "crm:P2 has type",
            "fo:description",
            "crm:P45 consists of",
            "fo:budget",
            "fo:duration",
            "fo:title",
            "rico:measure",
            "rico:identifier",
            "rdfs:label",
            "mo:duration",
            "mo:musicbrainz_guid",
            "rico:conditionsOfUse",
            "rico:conditionsOfAccess",
            "rico:generalDescription",
            "rico:scopeAndContent",
            "rico:hasOrHadSubject"]
prefix_dict = {"fo":fo, "mo":mo, "fabio":fabio, "schema":schema, "dcterms":dcterms,
                    "rico":rico, "crm":crm, "rdfs":rdfs, "lode":lode}

def urificator(csv_files:list):
    count = 0
    for file in csv_files:
        rows = []
        with open(file, mode = "r", encoding = "utf-8") as file_csv:
            f = csv.reader(file_csv)
            header = next(f)
            for triple in f:
                predicate = triple[1].replace(" ", "_")
                subject = path + triple[0].replace(" ", "-") + ">"
                if not predicate in literals:
                    object = path + triple[2].replace(" ", "-") + ">"
                else:
                    object = triple[2]
                row = [subject, predicate, object]
                rows.append(row)
            filename = f"item{count}.csv"
        with open(filename, "w", encoding="utf-8", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)
            csvwriter.writerows(rows)
        count+=1

def rdf_producer(csv_files:list):
    rdf_graph = rdflib.Graph()
    for prefix in prefix_dict:
        rdf_graph.bind(prefix, prefix_dict[prefix])
    for file in csv_files:
        with open(file, mode = "r", encoding="utf-8") as csv_file:
            f = csv.reader(csv_file)
            header = next(f)
            for triple in f:
                subject = triple[0][1:-1]
                print(subject)
                o = triple[1]
                ontology = prefix_dict[o[:o.index(":")]]
                predicate = triple[1][triple[1].index(":") + 1:]
                if triple[2].startswith("<"):
                    object = URIRef(triple[2][1:-1])
                else:
                    object = Literal(triple[2])
                rdf_graph.add((URIRef(subject), ontology[predicate], object))
    rdf_graph.serialize(destination="items.ttl", format="turtle")

def rdf_visualiser(rdf_file):

    # Apri il tuo file .ttl
    with open(rdf_file, 'r', encoding="utf-8") as file:
        data = file.read()

    # Invia una richiesta POST al servizio
    response = requests.post(f"http://www.ldf.fi/service/rdf-grapher?rdf={data}&from=ttl&to=png")

    # Controlla se la richiesta è andata a buon fine
    if response.status_code == 200:
        # Salva l'immagine del grafo
        with open('rdf_graph.png', 'wb') as f:
            f.write(response.content)
    else:
        print("Si è verificato un errore:", response.status_code)
        
