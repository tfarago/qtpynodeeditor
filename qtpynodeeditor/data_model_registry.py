import logging

from .node_data import NodeDataModel, NodeDataType
from .type_converter import TypeConverter

logger = logging.getLogger(__name__)


class DataModelRegistry:
    def __init__(self):
        self.type_converters = {}
        self._models_category = {}
        self._item_creators = {}
        self._categories = set()

    def register_model(self, creator, category='', *, style=None, **init_kwargs):
        name = creator.name
        self._item_creators[name] = (creator, {'style': style, **init_kwargs})
        self._categories.add(category)
        self._models_category[name] = category

    def register_type_converter(self, type_in: NodeDataType, type_out:
                                NodeDataType, type_converter: TypeConverter):
        """
        Register type converter

        Parameters
        ----------
        id_ : NodeData subclass or TypeConverterId
        type_converter : TypeConverter
        """
        # TODO typing annotation
        if hasattr(type_in, 'type'):
            type_in = type_in.type
        if hasattr(type_out, 'type'):
            type_out = type_out.type

        self.type_converters[(type_in, type_out)] = type_converter

    def create(self, model_name: str) -> NodeDataModel:
        """
        Create

        Parameters
        ----------
        model_name : str

        Returns
        -------
        value : (NodeDataModel, init_kwargs)
        """
        cls, kwargs = self._item_creators[model_name]
        return cls(**kwargs)

    def registered_model_creators(self) -> dict:
        """
        Registered model creators

        Returns
        -------
        value : dict
        """
        return dict(self._item_creators)

    def registered_models_category_association(self) -> dict:
        """
        Registered models category association

        Returns
        -------
        value : DataModelRegistry.RegisteredModelsCategoryMap
        """
        return self._models_category

    def categories(self) -> set:
        """
        Categories

        Returns
        -------
        value : DataModelRegistry.CategoriesSet
        """
        return self._categories

    def get_type_converter(self, d1: NodeDataType, d2: NodeDataType) -> TypeConverter:
        """
        Get type converter

        Parameters
        ----------
        d1 : NodeDataType
        d2 : NodeDataType

        Returns
        -------
        value : TypeConverter
        """
        return self.type_converters.get((d1, d2), None)
