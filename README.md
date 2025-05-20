# warc-metadata2rdf

`warc-metadata2rdf` is a command-line tool that extracts structured metadata from WARC files and serializes it as RDF using the [DOWARC vocabulary](https://github.com/DOWARC/dowarc). It supports various RDF output formats including Turtle, RDF/XML, N-Triples, and Notation3.

The goal is to produce semantically rich descriptions of WARC records for downstream processing, SPARQL querying, linked data publication, or archival analysis.

---

## Features

- Parses WARC headers using [`warcio`](https://github.com/webrecorder/warcio)
- Maps headers to RDF classes using a local OWL vocabulary
- Outputs RDF in `turtle`, `xml`, `nt`, or `n3` format
- Automatically handles unsafe or invalid URIs
- Compatible with DOWARC-compliant RDF graphs

---

## Installation

Requires [Poetry](https://python-poetry.org/) for dependency management.

```bash
git clone https://github.com/FabioKn/warc-metadata2rdf.git
cd warc-metadata2rdf
poetry install
```

---

## Usage

```bash
poetry run warc2rdf -i <input.warc.gz> -o <output.ttl>
```

### Options

| Option             | Description                                                    |
|--------------------|----------------------------------------------------------------|
| `-i`, `--input`    | Path to the WARC or WARC.GZ file                               |
| `-o`, `--output`   | Path to the RDF output file                                    |
| `-f`, `--format`   | RDF format: `turtle`, `xml`, `nt`, `n3` (default: `turtle`)    |

### Example

```bash
poetry run warc2rdf \
  -i example1.warc.gz \
  -o example1.ttl \
  -f turtle
```

---

## RDF Output (Turtle Example)

```ttl
<urn:uuid:656be776-49aa-4236-b55c-be1e82eb456b> a dowarc:WARCrecord ;
  ore:aggregates [
    a dowarc:WARC-Block-Digest ;
    rdfs:label "urn:uuid:656be776-..._WARC-Block-Digest"@en ;
    rdf:value "sha1:..."^^xsd:string
  ] .
```

---

## Vocabulary

This tool relies on the [DOWARC vocabulary](https://github.com/DOWARC/dowarc), included as an OWL file. By default, it expects the file to be located at:

```
warcmetadata/vocab/dowarc.owl
```

You can change this path by modifying the `load_dowarc_mapping()` function.

---

## License

This project is licensed under the **[European Union Public License v1.2 (EUPL-1.2)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)**.

You are free to use, modify, and redistribute this software under the terms of the EUPL. It is compatible with the GPL, AGPL, and most major open source licenses.

---

## Author

Fabio Knöß  
Developed as part of a metadata and web archiving project at the German National Library (DNB).

---

## Acknowledgements

- [warcio](https://github.com/webrecorder/warcio) - WARC parser
- [rdflib](https://github.com/RDFLib/rdflib) - RDF framework for Python
- [DOWARC](https://github.com/DOWARC/dowarc) - RDF vocabulary for web archive metadata
