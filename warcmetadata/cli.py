import click
from warcio.archiveiterator import ArchiveIterator
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD
from urllib.parse import urlparse

# Define namespaces
DOWARC = Namespace("https://github.com/DOWARC/dowarc#")
ORE = Namespace("http://www.openarchives.org/ore/terms/")

def load_dowarc_mapping(path_to_owl="warcmetadata/vocab/dowarc.owl"):
    """
    Load RDF vocabulary and map WARC header labels to ontology URIs.
    """
    g = Graph()
    g.parse(path_to_owl)

    mapping = {}
    for s, p, o in g.triples((None, RDFS.label, None)):
        if isinstance(o, str) and "WARC-" in o:
            mapping[o.strip()] = s
    return mapping

def safe_uri_or_bnode(value: str):
    """
    Return URIRef if value is serializable, else fall back to BNode.
    Prevents rdflib crashes on invalid or unsafe URIs.
    """
    try:
        parsed = urlparse(value)
        if not parsed.scheme or not parsed.path:
            raise ValueError("Invalid URI format")

        uri = URIRef(value)
        _ = uri.n3()  # Check if rdflib can serialize it
        return uri
    except Exception:
        # Optional: click.echo(f"?? Unsafe URI: {value} ? using BNode", err=True)
        return BNode()

@click.command(help="Extract metadata from a WARC file and serialize it using the DOWARC vocabulary.")
@click.option('--input', '-i', 'warc_path', required=True, type=click.Path(exists=True),
              help='Path to the input WARC (.warc or .warc.gz) file.')
@click.option('--output', '-o', 'output_path', required=True, type=click.Path(),
              help='Path to the output RDF file.')
@click.option('--format', '-f', 'rdf_format', default="xml", show_default=True,
              type=click.Choice(["xml", "turtle", "nt", "n3"], case_sensitive=False),
              help='Optional RDF serialization format.')
def extract_metadata(warc_path, output_path, rdf_format):
    """
    Main CLI entrypoint: reads WARC file, extracts metadata, builds RDF, serializes graph.
    """
    graph = Graph()
    graph.bind("dowarc", DOWARC)
    graph.bind("ore", ORE)

    mapping = load_dowarc_mapping()

    with open(warc_path, "rb") as stream:
        for record in ArchiveIterator(stream):
            record_id = record.rec_headers.get("WARC-Record-ID")
            if not record_id:
                continue

            record_uri = safe_uri_or_bnode(record_id)
            graph.add((record_uri, RDF.type, DOWARC.Record))

            for key, value in record.rec_headers.headers:
                if key in mapping:
                    prop_uri = mapping[key]
                    val_node = safe_uri_or_bnode(value)
                    label_str = f"{record_id}_{key}"

                    graph.add((val_node, RDF.type, prop_uri))
                    graph.add((val_node, RDFS.label, Literal(label_str, lang="en")))

                    # Type inference
                    if "Date" in key:
                        lit = Literal(value, datatype=XSD.dateTime)
                    elif "Length" in key:
                        lit = Literal(value, datatype=XSD.integer)
                    else:
                        lit = Literal(value)

                    graph.add((val_node, RDF.value, lit))
                    graph.add((record_uri, ORE.aggregates, val_node))

    graph.serialize(destination=output_path, format=rdf_format)
    click.echo(f"Metadata exported to: {output_path} (Format: {rdf_format})")

if __name__ == "__main__":
    extract_metadata()
