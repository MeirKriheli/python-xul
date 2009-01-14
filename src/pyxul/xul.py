"""XUL widgets implementation"""
from pyxul.widget import Widget, NS_MAP

class Window(Widget):
    """Extends Widget to take into account the onload, script and
    xml namespaces.

    """
    tag = 'window'

    def _render_openning(self, depth):
        """Add name spaces to the window declaration"""
        xml = super(Window, self)._render_openning(depth)
        for namespace, prefix in NS_MAP.items():
            if prefix:
                ns_prefix = ':' + prefix
            else:
                ns_prefix = ''

            xml += ' xmlns%s="%s"' % (ns_prefix, namespace)

        return xml



# The following is taken from nufox (thanks) at:
# http://svn.berlios.de/wsvn/nufox/trunk/nufox/xul.py
#
# For each widget that has not yet been defined from our big list of
# XUL tags, create a widget class that behaves like a good widget
# should and does nothing fancy.
XUL_TAGS = [
    'Action', 'ArrowScrollBox', 'BBox', 'Binding',
    'Bindings', 'Box', 'Broadcaster', 'BroadcasterSet', 'Button',
    'Browser', 'Checkbox', 'Caption', 'ColorPicker', 'Column', 'Columns',
    'CommandSet', 'Command', 'Conditions', 'Content', 'Deck',
    'Description', 'Dialog', 'DialogHeader', 'Editor', 'Grid', 'Grippy',
    'GroupBox', 'HBox', 'IFrame', 'Image', 'Key', 'KeySet', 'Label',
    'ListBox', 'ListCell', 'ListCol', 'ListCols', 'ListHead',
    'ListHeader', 'ListItem', 'Member', 'Menu', 'MenuBar', 'MenuItem',
    'MenuList', 'MenuPopup', 'MenuSeparator', 'Observes', 'Overlay',
    'Page', 'Popup', 'PopupSet', 'ProgressMeter', 'Radio', 'RadioGroup',
    'Resizer', 'Row', 'Rows', 'Rule', 'Script', 'Scrollbar', 'Scrollbox',
    'Separator', 'Spacer', 'Splitter', 'Stack', 'StatusBar',
    'StatusBarPanel', 'StringBundle', 'StringBundleSet', 'Tab',
    'TabBrowser', 'TabBox', 'TabPanel', 'TabPanels', 'Tabs', 'Template',
    'TextNode', 'TextBox', 'TitleBar', 'ToolBar', 'ToolBarButton',
    'ToolBarGrippy', 'ToolBarItem', 'ToolBarPalette', 'ToolBarSeparator',
    'ToolbarSet', 'ToolBarSpacer', 'ToolBarSpring', 'ToolBox', 'ToolTip',
    'Tree', 'TreeCell', 'TreeChildren', 'TreeCol', 'TreeCols', 'TreeItem',
    'TreeRow', 'TreeSeparator','Triple', 'VBox', 'Window', 'Wizard',
    'WizardPage',
    ]

GLOBALS = globals()

for tag in XUL_TAGS:
    if tag not in GLOBALS.keys():
        GLOBALS[tag] = type(tag, (Widget,), {'tag' : tag.lower()})

