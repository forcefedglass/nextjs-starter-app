from krita import Extension
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMenu, QAction
from PyQt5.QtCore import Qt, pyqtSignal
import logging

class PanelManagerExtension(Extension):
    """
    Main extension class for the Krita Dynamic Panel Manager.
    Handles plugin initialization, menu actions, and panel management.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.panel_columns = {}  # Dictionary to track panel columns
        self.setupLogger()
        
    def setupLogger(self):
        """Initialize logging for the extension"""
        self.logger = logging.getLogger("PanelManagerExtension")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def setup(self):
        """
        Called by Krita to setup the extension.
        Registers actions and initializes the panel system.
        """
        try:
            self.logger.info("Setting up Krita Dynamic Panel Manager")
            
            # Register actions in Krita's menu
            if not Krita.instance():
                self.logger.error("Failed to get Krita instance")
                return

            # Create and register menu actions
            self.registerMenuActions()
            
            # Initialize default panel layout
            self.createDefaultLayout()
            
        except Exception as e:
            self.logger.error(f"Error during setup: {str(e)}")

    def registerMenuActions(self):
        """Register menu actions for the plugin"""
        try:
            # Add Panel action
            self.addPanelAction = QAction("Add Panel Column", self.parent())
            self.addPanelAction.triggered.connect(self.addPanelColumn)
            
            # Remove Panel action
            self.removePanelAction = QAction("Remove Panel Column", self.parent())
            self.removePanelAction.triggered.connect(self.removePanelColumn)
            
            # Reset Layout action
            self.resetLayoutAction = QAction("Reset Layout", self.parent())
            self.resetLayoutAction.triggered.connect(self.resetLayout)
            
            # Add actions to Krita's View menu
            window = Krita.instance().activeWindow()
            if window:
                menu = window.qwindow().menuBar().addMenu("Panel Manager")
                menu.addAction(self.addPanelAction)
                menu.addAction(self.removePanelAction)
                menu.addSeparator()
                menu.addAction(self.resetLayoutAction)
                
        except Exception as e:
            self.logger.error(f"Error registering menu actions: {str(e)}")

    def createDefaultLayout(self):
        """Create the default panel layout with one column"""
        try:
            # Create initial panel column
            self.addPanelColumn()
        except Exception as e:
            self.logger.error(f"Error creating default layout: {str(e)}")

    def addPanelColumn(self):
        """Add a new panel column if under the limit"""
        try:
            if len(self.panel_columns) >= 8:
                self.logger.warning("Maximum number of panel columns (8) reached")
                return False
                
            column_id = len(self.panel_columns) + 1
            from .drag_drop_panel_widget import DragDropPanelWidget
            
            new_column = DragDropPanelWidget(parent=self.parent())
            self.panel_columns[column_id] = new_column
            
            # Position the new column
            self.updateColumnPositions()
            
            self.logger.info(f"Added new panel column {column_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding panel column: {str(e)}")
            return False

    def removePanelColumn(self, column_id=None):
        """Remove the specified panel column or the last one if not specified"""
        try:
            if not self.panel_columns:
                self.logger.warning("No panel columns to remove")
                return False
                
            if column_id is None:
                column_id = max(self.panel_columns.keys())
                
            if column_id in self.panel_columns:
                column = self.panel_columns.pop(column_id)
                column.deleteLater()
                self.updateColumnPositions()
                self.logger.info(f"Removed panel column {column_id}")
                return True
            else:
                self.logger.warning(f"Panel column {column_id} not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Error removing panel column: {str(e)}")
            return False

    def updateColumnPositions(self):
        """Update the positions of all panel columns"""
        try:
            window = Krita.instance().activeWindow()
            if not window:
                return
                
            main_window = window.qwindow()
            screen_width = main_window.width()
            
            # Calculate column width based on number of columns
            column_width = screen_width // max(len(self.panel_columns), 1)
            
            # Position each column
            for idx, column in self.panel_columns.items():
                x_pos = (idx - 1) * column_width
                column.setGeometry(x_pos, 0, column_width, main_window.height())
                
        except Exception as e:
            self.logger.error(f"Error updating column positions: {str(e)}")

    def resetLayout(self):
        """Reset to default layout with one panel column"""
        try:
            # Remove all existing columns
            for column_id in list(self.panel_columns.keys()):
                self.removePanelColumn(column_id)
                
            # Create default layout
            self.createDefaultLayout()
            self.logger.info("Layout reset to default")
            
        except Exception as e:
            self.logger.error(f"Error resetting layout: {str(e)}")

    def canvasChanged(self, canvas):
        """Handle canvas change events"""
        try:
            if canvas:
                self.updateColumnPositions()
        except Exception as e:
            self.logger.error(f"Error handling canvas change: {str(e)}")
