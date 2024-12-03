"""Source assignments for transforms."""

BAD_PREFIXES = [
    "DATA",
    "OBAN",
    "OIO",
    "PHENIO",
    "WD_Entity",
    "WD_Prop",
    "biolink",
    "chebi#is",
    "core#connected",
    "core#distally",
    "core#innervated",
    "core#subdivision",
    "dc",
    "dcat",
    "dcterms",
    "dctypes",
    "doid#derives",
    "doid#has",
    "emapa#Tmp",
    "emapa#group",
    "emapa#group_term",
    "foaf",
    "http",
    "https",
    "mondo#disease",
    "nbo#by",
    "nbo#has",
    "nbo#in",
    "nbo#is",
    "ncit#C142749",
    "rdf",
    "rdfs",
    "stato.owl#is",
    "stato.owl#response",
]

EDGE_SOURCES = {
    "APO": "apo",  # Ascomycete phenotype ontology - cat only
    "BFO": "bfo",
    "BSPO": "upheno",  # Biological Spatial Ontology - from Upheno
    "BTO": "bto",  # BRENDA vocab - cat only
    "CARO": "caro",  # CARO - cat only
    "CHEBI": "chebi",
    "CHR": "mondo",  # Chromosome ID - from MONDO
    "CIO": "cio",  # Confidence Information - cat only
    "CL": "cl",
    "CLO": "clo",  # Cell Line - cat only
    "COB": "cob",
    "DDANAT": "ddanat",  # Dictyostelium discoideum anatomy - cat only
    "DDPHENO": "ddpheno",
    "DOID": "doid",  # Disease ID - cat only
    "ECO": "eco",
    "ECTO": "ecto",
    "ExO": "exo",
    "EMAPA": "emapa",
    "ENVO": "envo",
    "FAO": "fao",
    "FBbt": "fbbt",
    "FBcv": "fbcv",
    "FBdv": "fbdv",
    "FMA": "fma",
    "FOODON": "foodon",
    "FlyBase": "flybase",
    "FYPO": "fypo",
    "GENO": "geno",
    "GO": "go",
    "GOREL": "go",
    "HP": "hp",
    "HsapDv": "HsapDv",
    "IAO": "iao",
    "INO": "ino",
    "MA": "ma",
    "MAXO": "maxo",
    "MF": "mf",
    "MFOMD": "mondo",  # Mental Disease - ref'd by MONDO
    "MI": "mi",
    "MOD": "mod",
    "MONDO": "mondo",
    "MP": "mp",
    "MPATH": "mpath",
    "NBO": "nbo",
    "NCBITaxon": "ncbitaxon",
    "NCIT": "ncit",
    "OBA": "oba",
    "OBAN": "oban",
    "OBI": "obi",
    "OBO": "unknown",  # a messy one - may not be OBO though
    "OGMS": "ogms",
    "OIO": "oio",
    "OMIM": "omim",  # OMIM - cat only
    "OMIT": "omit",
    "Orphanet": "orphanet",
    "PATO": "pato",
    "PCO": "pco",
    "PO": "po",
    "PR": "pr",
    "PW": "pw",
    "RO": "ro",
    "RnorDv": "rnordv",
    "RXCUI": "rxnorm",  # RXNORM - cat only
    "SEPIO": "sepio",
    "SO": "so",
    "SIO": "sio",
    "SNOMED": "snomed",
    "STATO": "stato",
    "TO": "to",  # Plant Trait - cat only
    "TS": "ts",  # almost always with EMAPA
    "UBERON": "uberon",
    "UMLS": "umls",  # UMLS - cat only
    "UPHENO": "upheno",
    "WBPhenotype": "wbphenotype",
    "WBBT": "wbbt",
    "WBbt": "wbbt",
    "WBls": "wbls",
    "XAO": "xao",
    "XCO": "xco",
    "XPO": "xpo",
    "ZFA": "zfa",
    "ZFS": "zfs",
    "ZP": "zp",
    "biolink": "biolink",
    "dcat": "dcat",
    "dcterms": "dcterms",
    "dctypes": "dctypes",
    "faldo": "faldo",
    "foaf": "foaf",
    "owl": "owl",
    "pav": "pav",  # PAV onto - cat only
    "rdf": "rdf",
    "rdfs": "rdfs",
    "skos": "skos",
}

# In each of the following, the key is the prefix,
# the first value of the tuple is the source to be used as infores,
# and the second is the category.
# One source may be used with multiple categories;
# the one defined here is essentially the "default" category.
NODE_SOURCES = {
    "APO": ("apo", ""),
    "BFO": ("bfo", ""),
    "BSPO": ("bspo", ""),
    "BTO": ("bto", ""),
    "CARO": ("caro", ""),
    "CHEBI": ("chebi", "ChemicalEntity"),
    "CHR": ("chr", "MolecularEntity"),
    "CIO": ("cio", ""),
    "CL": ("cl", ""),
    "CLO": ("clo", ""),
    "DDANAT": ("ddanat", ""),
    "DDPHENO": ("ddpheno", "PhenotypicFeature"),
    "DOID": ("doid", "Disease"),
    "ECO": ("eco", ""),
    "EMAPA": ("emapa", "AnatomicalEntity"),
    "ENVO": ("envo", "EnvironmentalFeature"),
    "FAO": ("fao", ""),
    "FBbt": ("fbbt", "AnatomicalEntity"),
    "FBcv": ("fbcv", ""),
    "FBdv": ("fbdv", ""),
    "FBgn": ("fbgn", "Gene"),
    "FMA": ("fma", ""),
    "FOODON": ("foodon", ""),
    "FlyBase": ("flybase", ""),
    "FYPO": ("fypo", "PhenotypicFeature"),
    "GENO": ("geno", ""),
    "GO": ("go", ""),
    "HGNC": ("hgnc", "Gene"),
    "HP": ("hp", "PhenotypicFeature"),
    "HsapDv": ("hsapdv", "LifeStage"),
    "IAO": ("iao", ""),
    "MA": ("ma", "AnatomicalEntity"),
    "MF": ("mf", ""),
    "MFOMD": ("mfomd", ""),
    "MI": ("mi", ""),
    "MOD": ("mod", ""),
    "MONDO": ("mondo", "Disease"),
    "MP": ("mp", "PhenotypicFeature"),
    "MPATH": ("mpath", "Disease"),
    "NBO": ("nbo", "PhenotypicFeature"),
    "NCBITaxon": ("ncbitaxon", ""),
    "NCIT": ("ncit", ""),
    "OBA": ("oba", ""),
    "OBAN": ("oban", ""),
    "OBI": ("obi", ""),
    "OBO": ("obo", ""),  # TODO: clean this up
    "OGMS": ("ogms", ""),
    "OIO": ("oio", ""),
    "OMIM": ("omim", ""),
    "OMIT": ("omit", ""),
    "Orphanet": ("orphanet", ""),
    "PATO": ("pato", ""),
    "PCO": ("pco", ""),
    "PO": ("po", ""),
    "PR": ("pr", "Protein"),
    "PW": ("pw", ""),
    "RO": ("ro", ""),
    "RXCUI": ("rxnorm", ""),
    "SEPIO": ("sepio", ""),
    "SNOMED": ("snomed", ""),
    "SO": ("so", "MolecularEntity"),
    "SIO": ("sio", ""),
    "STATO": ("stato", ""),
    "TO": ("to", ""),
    "UBERON": ("uberon", "AnatomicalEntity"),
    "UMLS": ("umls", ""),
    "UPHENO": ("upheno", "PhenotypicFeature"),
    "WBPhenotype": ("wbphenotype", "PhenotypicFeature"),
    "WBBT": ("wbbt", "AnatomicalEntity"),
    "WBbt": ("wbbt", "AnatomicalEntity"),
    "XAO": ("xao", "AnatomicalEntity"),
    "XCO": ("xco", ""),
    "XPO": ("xpo", "PhenotypicFeature"),
    "ZFA": ("zfa", "AnatomicalEntity"),
    "ZFS": ("zfs", "LifeStage"),
    "ZP": ("zp", "PhenotypicFeature"),
    "biolink": ("biolink", ""),
    "faldo": ("faldo", ""),
    "owl": ("owl", ""),
    "pav": ("pav", ""),
    "skos": ("skos", ""),
}
