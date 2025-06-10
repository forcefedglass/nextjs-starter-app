import json
import os
import logging
from PyQt5.QtCore import QRect, QPoint, QSize

class PanelLayoutManager:
    """
    Manages saving and loading of panel layouts.
    Handles serialization of panel positions, sizes, and configurations.
    """
    
    def __init__(self):
        self.setupLogger()
        self.config_path = self._get_config_path()
        
    def setupLogger(self):
        """Initialize logging for the layout manager"""
        self.logger = logging.getLogger("PanelLayoutManager")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
    def _get_config_path(self):
        """Get the path for the configuration file"""
        try:
            # Get Krita's resource folder
            config_dir = os.path.expanduser("~/.local/share/krita/panel_manager")
            os.makedirs(config_dir, exist_ok=True)
            return os.path.join(config_dir, "panel_layout.json")
        except Exception as e:
            self.logger.error(f"Error getting config path: {str(e)}")
            return None
            
    def saveLayout(self, panel_columns):
        """
        Save the current panel layout configuration
        
        Args:
            panel_columns (dict): Dictionary of panel columns and their configurations
        """
        try:
            if not self.config_path:
                raise ValueError("Configuration path not set")
                
            layout_data = {}
            
            # Convert panel data to serializable format
            for column_id, panel in panel_columns.items():
                geometry = panel.geometry()
                layout_data[str(column_id)] = {
                    'x': geometry.x(),
                    'y': geometry.y(),
                    'width': geometry.width(),
                    'height': geometry.height(),
                    'visible': panel.isVisible()
                }
                
            # Save to file
            with open(self.config_path, 'w') as f:
                json.dump(layout_data, f, indent=4)
                
            self.logger.info("Layout saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving layout: {str(e)}")
            return False
            
    def loadLayout(self):
        """
        Load the saved panel layout configuration
        
        Returns:
            dict: Layout configuration data or None if loading fails
        """
        try:
            if not self.config_path or not os.path.exists(self.config_path):
                self.logger.info("No saved layout found, using default")
                return None
                
            with open(self.config_path, 'r') as f:
                layout_data = json.load(f)
                
            # Convert loaded data back to usable format
            converted_layout = {}
            for column_id, data in layout_data.items():
                converted_layout[int(column_id)] = {
                    'geometry': QRect(
                        data['x'],
                        data['y'],
                        data['width'],
                        data['height']
                    ),
                    'visible': data['visible']
                }
                
            self.logger.info("Layout loaded successfully")
            return converted_layout
            
        except Exception as e:
            self.logger.error(f"Error loading layout: {str(e)}")
            return None
            
    def getDefaultLayout(self):
        """
        Get the default layout configuration
        
        Returns:
            dict: Default layout configuration
        """
        try:
            # Create a simple default layout with one column
            return {
                1: {
                    'geometry': QRect(0, 0, 200, 600),
                    'visible': True
                }
            }
        except Exception as e:
            self.logger.error(f"Error creating default layout: {str(e)}")
            return None
            
    def validateLayout(self, layout_data):
        """
        Validate the layout configuration
        
        Args:
            layout_data (dict): Layout configuration to validate
            
        Returns:
            bool: True if layout is valid, False otherwise
        """
        try:
            if not isinstance(layout_data, dict):
                return False
                
            # Check maximum number of columns
            if len(layout_data) > 8:
                return False
                
            # Validate each column's data
            for column_id, data in layout_data.items():
                if not isinstance(column_id, int):
                    return False
                    
                required_keys = {'geometry', 'visible'}
                if not all(key in data for key in required_keys):
                    return False
                    
                if not isinstance(data['geometry'], QRect):
                    return False
                    
                if not isinstance(data['visible'], bool):
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating layout: {str(e)}")
            return False
            
    def clearSavedLayout(self):
        """Delete the saved layout configuration file"""
        try:
            if self.config_path and os.path.exists(self.config_path):
                os.remove(self.config_path)
                self.logger.info("Saved layout cleared")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error clearing saved layout: {str(e)}")
            return False
