from django.template import Library, Node, Variable, VariableDoesNotExist
from django.core.urlresolvers import reverse

from job_board.views import job_list_by_tag

register = Library()

def do_populate_tags(parser,token):
    """
    render a list of tags, with it's link.
    the token is tag.
    Arguments:
    - `parser`:
    - `token`:
    """
    bits = token.split_contents()
    print bits
    return PopulateTagsNode(bits[1])

class PopulateTagsNode(Node):
    def __init__(self,tag):
        self.tag_tag = Variable(tag)

    def render(self,context):
        try:
            _tag = self.tag_tag.resolve(context)
            _font_size = _tag.font_size + 10
            _font_weight = min(900,(300 + (_tag.font_size*100)))
            _url = reverse(job_list_by_tag, kwargs = {'tag_name' : _tag.name} )

            return "<span style='font-size:%spx;font-weight:%s'><a href='%s'>%s</a></span>" % (_font_size,_font_weight,_url,_tag.name)
        except VariableDoesNotExist:
            return ''

register.tag('populate_tag', do_populate_tags)