"""Implements behavior common to all application classes.."""

from abc import ABC, abstractmethod
from event_ticketing.logging import LoggingService
from event_ticketing.settings import Settings

class ApplicationBase(ABC):
    """Implements ApplicationBase class."""
    
    def __init__(self, subclass_name:str, logfile_prefix_name:str)->None:
        """Instantiate instance."""
        self._settings = Settings().read_settings_file_from_location()
        self._logger = LoggingService(subclass_name, logfile_prefix_name)
        
       
    



    