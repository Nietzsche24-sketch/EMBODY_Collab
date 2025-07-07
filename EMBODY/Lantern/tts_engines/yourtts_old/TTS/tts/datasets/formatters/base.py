class BaseDatasetFormatter:
    def parse_item(self, line, root_path, meta_path):
        raise NotImplementedError("Subclasses should implement this!")
