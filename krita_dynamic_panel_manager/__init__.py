from .panel_manager_extension import PanelManagerExtension

# Entry point for Krita to load the plugin
def createPlugin(parent):
    return PanelManagerExtension(parent)
