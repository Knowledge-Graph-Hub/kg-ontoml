"""Koza transform for adding knowledge sources to PHENIO."""

import importlib

from koza.cli_utils import get_koza_app  # type: ignore

from kg_phenio.transform_utils.sources import BAD_PREFIXES, NODE_SOURCES

source_name = "phenio_node_sources"

SYNONYM = "synonym"

koza_app = get_koza_app(source_name)


# This transform is for enriching PHENIO-derived nodes with:
# * Biolink-compliant knowledge sources, in the provided_by slot.
# * Biolink categories, in the category slot.

# This maps CURIE prefixes to infores: names and categories.
infores_sources = {key: value[0] for key, value in NODE_SOURCES.items()}
category_sources = {key: value[1] for key, value in NODE_SOURCES.items()}

primary_knowledge_source = "infores:unknown"

while (row := koza_app.get_row()) is not None:

    try:
        node_curie_prefix, node_curie_value = str(row["id"]).split(":")
    except ValueError as e:  # Catch any malformed CURIEs
        print(f"Error: {e}")
        print(f"Row: {row}")
        continue
    category_name = (str(row["category"]).split(":"))[1]

    # Catch some IDs first before we ignore them
    if str(row["id"]).startswith("http://identifiers.org/hgnc/"):
        node_curie_prefix = "HGNC"
        node_curie_value = str(row["id"]).split("/")[-1]

    identifier = f"{node_curie_prefix}:{node_curie_value}"

    if node_curie_prefix in BAD_PREFIXES:
        continue

    # Many categories may still have a generic NamedThing,
    # or other generic category.
    # We can assign a more specific category.
    remap_cats = ["OntologyClass", "NamedThing", "ChemicalSubstance", "SequenceFeature"]

    if category_name in remap_cats:
        if category_name == "OntologyClass":
            category_name = "NamedThing"
        if node_curie_prefix == "FlyBase":  # Look at ID to get the category
            if node_curie_value.startswith("FBgn"):
                node_curie_prefix = "FBgn"
        if node_curie_prefix == "OBO":  # Look at ID to get the category
            if node_curie_value.startswith("XPO"):
                node_curie_prefix = "XPO"
            elif node_curie_value.startswith("HsapDv"):
                node_curie_prefix = "HsapDv"
        if category_sources[node_curie_prefix]:
            category_name = category_sources[node_curie_prefix]

    # TODO: make this more specific
    infores = infores_sources[node_curie_prefix]
    primary_knowledge_source = f"infores:{infores}"

    # Write the node
    # The category tells us which class to use.
    # Get the class from the model
    NodeClass = getattr(
        importlib.import_module("biolink_model.datamodel.pydanticmodel_v2"),
        category_name,
    )

    node = NodeClass(
        id=identifier,
        category=["biolink:" + category_name],
        name=row["name"],
        description=row["description"],
        # turning empty strings into False feels wrong, keeping them empty
        deprecated=bool(row["deprecated"]) if row["deprecated"] else None,
        provided_by=[primary_knowledge_source],
    )

    all_slots = list(node.__dict__.keys())
    if row["iri"]:
        node.iri = row["iri"]
    if row[SYNONYM] and SYNONYM in all_slots:
        node.synonym = (row["synonym"]).split("|")

    if row["subsets"]:
        subsets = (row["subsets"]).split("|")

        if "deprecated" in subsets:
            node.deprecated = True

    if row["xref"]:
        xrefs = (row["xref"]).split("|")
        node.xref = xrefs

    koza_app.write(node)
