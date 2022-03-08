import os
from typing import Optional
from kg_ontoml.transform_utils.transform import Transform
from kgx.cli.cli_utils import transform # type: ignore

ONTO_FILES = {
    'MonarchTransform': 'monarch-merged.owl',
}

class MonarchTransform(Transform):
    """
    MonarchTransform parses the merged monarch.owl into nodes and edges.
    """
    def __init__(self, input_dir: str = None, output_dir: str = None):
        source_name = "monarch-merged"
        super().__init__(source_name, input_dir, output_dir)

    def run(self, data_file: Optional[str] = None) -> None:
        """Method is called and performs needed transformations to process
        an ontology.
        Args:
            data_file: data file to parse
        Returns:
            None.
        """
        if data_file:
            k = data_file.split('.')[0]
            data_file = os.path.join(self.input_base_dir, data_file)
            self.parse(k, data_file, k)
        else:
            # load all ontologies
            for k in ONTO_FILES.keys():
                data_file = os.path.join(self.input_base_dir, ONTO_FILES[k])
                self.parse(k, data_file, k)

    def parse(self, name: str, data_file: str, source: str) -> None:
        """Processes the data_file.
        Args:
            name: Name of the ontology
            data_file: data file to parse
            source: Source name
        Returns:
             None.
        """
        print(f"Parsing {data_file}")
        
        transform(inputs=[data_file], input_format='owl', output= os.path.join(self.output_dir, name), output_format='tsv')