
from bot.db import Manager
from aiogram import types


class DataManager:
    def __init__(self, db_data: list[tuple]) -> None:
        """Initialize data manager"""
        self.delete_data = db_data
        self.new_data = []
        self.change_data = []
        
    def check_data(self, data: tuple) -> None:
        """Check data in database"""
        self.data = data
        self.it_is_changed()
    
    def it_is_changed(self) -> None:
        """Check if data is changed or not in database"""
        for index, item in enumerate(self.delete_data):
            if item[0] == self.data[0]:
                if item[2] != self.data[2]:
                    self.change_data.append(self.data)
                self.delete_data.pop(index)
                return None
        self.new_data.append(self.data)
    
    def consume_data_to_db(self, manager: Manager) -> None:
        """Consume data to database
        :param manager: database manager"""
        if self.new_data:
            manager.insert_data(self.new_data)
            
        if self.change_data:
            manager.change_price_data(self.change_data)
        
        if self.delete_data:
            manager.delete_data(self.delete_data) 
            
    def get_media(self, data: list, caption: str) -> types.MediaGroup:
        """Get media group
        :param data: list of tuples with data
        :param caption: caption for media group
        :return: media group
        """
        media = types.MediaGroup()
        media.attach_photo(data[5], caption=caption, parse_mode='HTML')
        media.attach_photo(data[6])
        media.attach_photo(data[7])
        media.attach_photo(data[8])
        media.attach_photo(data[9])
        return media
        