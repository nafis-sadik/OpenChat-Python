class IRepositoryBase:
    def get_version(self):
        raise NotImplementedError

    def create_database(self):
        raise NotImplementedError

    def add(self, data: any) -> None:
        raise NotImplementedError

    def delete(self, data: any) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def get_all(self) -> list:
        raise NotImplementedError

    def get_col(self, *conditions, **cols) -> list:
        raise NotImplementedError

    def get(self, *args) -> list:
        raise NotImplementedError

    def get_count(self) -> int:
        raise NotImplementedError

    def max(self, col_map) -> int:
        raise NotImplementedError
