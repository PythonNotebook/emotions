from . import mysql


class Images:
    @staticmethod
    def list_emojis_all(limit: int = 32, offset: int = 0) -> list[dict]:
        result = mysql.list_emojis_all(limit=limit, offset=offset)
        return result

    @staticmethod
    def list_emojis_by_character(i_character: str, limit: int = 32, offset: int = 0) -> list[dict]:
        result = mysql.list_emojis_by_character(i_character=i_character, limit=limit, offset=offset)
        return result

    @staticmethod
    def get_image_path_by_id(image_id: str) -> str:
        return mysql.get_image_path_by_id(image_id)
