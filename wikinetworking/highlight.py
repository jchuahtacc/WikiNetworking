import matplotlib
import mpld3

## A plugin that provides mouseover highlighting by altering fill opacity and stroke width and opacity
class Highlight(mpld3.plugins.PluginBase):

    JAVASCRIPT = """
    mpld3.register_plugin("highlight", Highlight);
    Highlight.prototype = Object.create(mpld3.Plugin.prototype);
    Highlight.prototype.constructor = Highlight;
    Highlight.prototype.requiredProps = ["id"];
    function Highlight(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    Highlight.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        urls = this.props.urls;
        var elems = obj.elements();
        for (var i = 0; i < elems[0].length; i++) {
            elems[0][i].onmouseover = function() {
                d3.select(this).transition().duration(100).style("fill-opacity", 1.0)
                    .style("stroke-opacity", 1.0)
                    .style("stroke-width", 3);
            }
            elems[0][i].onmouseout = function() {
                d3.select(this).transition().duration(200).style("fill-opacity", 0.3)
                    .style("stroke-opacity", 0.3)
                    .style("stroke-width", 1);
            }
        }
    }
    """

    ## A constructor for this plugin
    # @param    points      A list of items to provide highlighting behavior
    def __init__(self, points):
        self.points = points
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None
        self.dict_ = {"type": "highlight",
                      "id": mpld3.utils.get_id(points, suffix)}