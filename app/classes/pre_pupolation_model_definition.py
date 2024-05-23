from typing import List, Dict, Type, TypeVar, Any
from dataclasses import dataclass, fields

T = TypeVar('T', bound='BaseClass')


class BaseConfiguration:

    @staticmethod
    def from_dict(data_class: Type[T], data: Dict[str, Any]) -> T:
        """
        Helper function to instantiate a dataclass from a dictionary.
        """
        fieldtypes = {f.name: f.type for f in fields(data_class)}
        return data_class(**{f: BaseConfiguration.from_dict(
            fieldtypes[f], data[f]) if isinstance(data[f], dict) else data[f] for f in data})

@dataclass
class PrepopulationModelDefinition:
    model: str
    filters: Dict[str, str]


@dataclass
class PrepopulationConfiguration:
    process_name: str
    models: List[PrepopulationModelDefinition]
