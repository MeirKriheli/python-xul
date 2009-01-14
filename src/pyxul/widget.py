"""Basic XUL widget"""
from xml.sax.saxutils import escape

XUL_NS = "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul"
XHTML_NS = "http://www.w3.org/1999/xhtml"

NS_MAP =  {
    XUL_NS: None,
    XHTML_NS: 'html',
}

def _to_list(val):
    """Make sure the thing is iterable but not base string , otherwise return
    a list with the item as it's single element
    
    """

    if val is None:
        return []

    if isinstance(val, basestring):
        return [val]

    return val

class Widget(object):
    """Basic widget. This class can't instantiate, should be used
    as a basis for XUL/html elements.
    
    """
    NS  =  XUL_NS

    def __init__(self, **attributes):
        """Set attributes, seperate special attributes for normal (xml) ones.
            
        attributes -- attributes for this object.
        
        Special attributes which are not passed to XUL widget
        added to the rendered page:

        stylesheets -- extra stylesheets needed for this widget
        scripts -- extra java script files needed for this widget
        onload -- function call in case of onload
        head -- content before tag children
        tail -- content after tag children
        
        """

        # tag is required, sub classes must assign one
        tag = getattr(self, "tag", None)

        if not tag:
            raise NotImplementedError("widget tag is required")

        self.children = []
        self.parent = None
        self.head = None
        self.tail = None
        self.attributes = {}

        for attr, value in attributes.items():
            if attr in ['stylesheets', 'scripts', 'onload', 'head', 'tail']:
                setattr(self, attr, value)
            else:
                self.attributes[attr] = value

    def append(self, *widgets):
        """Append child widgets. Updates the `children` property and sets
        widgets parent.

        *widgets -- widgets to append to this widget

        """
        for widget in widgets:
            self.children.append(widget)
            widget.parent = self

        
    def append_to(self, parent):
        """Appends this widget to a parent
        
        parent -- parent widget
        """
        parent.append(self)
        
    def _render_openning(self, padding):
        """Renders the tag openning and attributes"""

        xml = "%s<%s" % (padding, getattr(self, "tag")) 
        for key, val in self.attributes.items():
            xml += ' %s="%s"' % (key, escape(val))

        return xml

    def _render_head(self, padding):
        """Returns list of head elemnts displayed before child widgets"""
        return [padding + ' ' + i for i in _to_list(self.head)]

    def _render_tail(self, padding):
        """Returns list of tail elemnts displayed after child widgets"""
        return [padding + ' ' +i for i in _to_list(self.tail)]

    def render(self, collect=None, padding=''):
        """yields widget to a string, calls child widgets render if needed.
        
        collect -- dictoionary for extra data collection (scripts, stylesheets
                   and onload)
        """

        if collect is None:
            collect = {'stylesheets':[], 'scripts':[], 'onload':[]}

        # update the collection
        for key in ['stylesheets', 'scripts', 'onload']:
            collect[key].extend( _to_list(getattr(self, key, None)))

        xml = self._render_openning(padding)

        if self.children or self.head or self.tail:
            xml += ">"

            yield xml
            for line in self._render_head(padding):
                yield line

            for child in self.children:
                for line in child.render(collect, padding+" "):
                    yield line

            for line in self._render_tail(padding):
                yield line

            yield '</%s>' % getattr(self, "tag")
        else:
            yield xml + '/>'
