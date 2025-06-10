from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizeGrip
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QPoint, QSize
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QColor, QPen
import logging

class DragDropPanelWidget(QWidget):
    """
    Custom widget that implements drag and drop functionality for panels.
    Supports resizing and visual feedback during drag operations.
    """
    
    # Custom signals
    panelMoved = pyqtSignal(object, QPoint)  # Emitted when panel is moved
    panelResized = pyqtSignal(object, QSize)  # Emitted when panel is resized
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupLogger()
        self.initUI()
        
    def setupLogger(self):
        """Initialize logging for the widget"""
        self.logger = logging.getLogger("DragDropPanelWidget")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
    def initUI(self):
        """Initialize the UI components"""
        try:
            # Enable dropping
            self.setAcceptDrops(True)
            
            # Main layout
            self.layout = QVBoxLayout(self)
            self.layout.setContentsMargins(5, 5, 5, 5)
            self.layout.setSpacing(0)
            
            # Content area
            self.content = QLabel("Panel Content")
            self.content.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.content)
            
            # Size grip for resizing
            self.sizeGrip = QSizeGrip(self)
            self.layout.addWidget(self.sizeGrip, 0, Qt.AlignBottom | Qt.AlignRight)
            
            # Set minimum size
            self.setMinimumSize(100, 100)
            
            # Apply styling
            self.applyStyle()
            
        except Exception as e:
            self.logger.error(f"Error initializing UI: {str(e)}")
            
    def applyStyle(self):
        """Apply custom styling to the widget"""
        try:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2a2a2a;
                    border: 1px solid #3a3a3a;
                    border-radius: 4px;
                }
                QWidget:hover {
                    border: 1px solid #4a4a4a;
                }
                QLabel {
                    color: #ffffff;
                    background-color: transparent;
                    border: none;
                    font-size: 12px;
                }
                QSizeGrip {
                    background-color: transparent;
                    border: none;
                }
            """)
        except Exception as e:
            self.logger.error(f"Error applying style: {str(e)}")
            
    def mousePressEvent(self, event):
        """Handle mouse press events to initiate drag operations"""
        try:
            if event.button() == Qt.LeftButton:
                self.dragStartPosition = event.pos()
        except Exception as e:
            self.logger.error(f"Error in mouse press event: {str(e)}")
            
    def mouseMoveEvent(self, event):
        """Handle mouse move events for drag operations"""
        try:
            if not (event.buttons() & Qt.LeftButton):
                return
                
            if (event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance():
                return
                
            # Create drag object
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText("panel")
            drag.setMimeData(mimeData)
            
            # Create drag pixmap with visual feedback
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            
            # Add semi-transparent effect
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
            painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 127))
            painter.end()
            
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            
            # Execute drag operation
            dropAction = drag.exec_(Qt.MoveAction)
            
        except Exception as e:
            self.logger.error(f"Error in mouse move event: {str(e)}")
            
    def dragEnterEvent(self, event):
        """Handle drag enter events"""
        try:
            if event.mimeData().hasText() and event.mimeData().text() == "panel":
                event.acceptProposedAction()
                self.highlightDropZone(True)
            else:
                event.ignore()
        except Exception as e:
            self.logger.error(f"Error in drag enter event: {str(e)}")
            
    def dragLeaveEvent(self, event):
        """Handle drag leave events"""
        try:
            self.highlightDropZone(False)
            event.accept()
        except Exception as e:
            self.logger.error(f"Error in drag leave event: {str(e)}")
            
    def dropEvent(self, event):
        """Handle drop events"""
        try:
            self.highlightDropZone(False)
            if event.mimeData().hasText() and event.mimeData().text() == "panel":
                self.panelMoved.emit(self, event.pos())
                event.acceptProposedAction()
            else:
                event.ignore()
        except Exception as e:
            self.logger.error(f"Error in drop event: {str(e)}")
            
    def highlightDropZone(self, highlight):
        """Toggle drop zone highlighting"""
        try:
            if highlight:
                self.setStyleSheet("""
                    QWidget {
                        background-color: #2a2a2a;
                        border: 2px solid #007acc;
                        border-radius: 4px;
                    }
                    QLabel {
                        color: #ffffff;
                        background-color: transparent;
                        border: none;
                        font-size: 12px;
                    }
                    QSizeGrip {
                        background-color: transparent;
                        border: none;
                    }
                """)
            else:
                self.applyStyle()
        except Exception as e:
            self.logger.error(f"Error highlighting drop zone: {str(e)}")
            
    def resizeEvent(self, event):
        """Handle resize events"""
        try:
            super().resizeEvent(event)
            self.panelResized.emit(self, event.size())
        except Exception as e:
            self.logger.error(f"Error in resize event: {str(e)}")
