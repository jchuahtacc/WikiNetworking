import matplotlib
import mpld3


## An mpld3 plugin that allows nodes to be clicked to open a URL
# Source: @link <http://stackoverflow.com/a/28838652/814354>
class ClickInfo(mpld3.plugins.PluginBase):
    """mpld3 Plugin for getting info on click
    Comes from:
        http://stackoverflow.com/a/28838652/814354
    """

    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id", "urls"];
    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        var urls = this.props.urls;
        var elems = obj.elements();
        elems.on("mousedown",
                          function(d, i){
                                window.open(urls[i], '_blank');
                            });
    }
    """

    ## A constructor for this plugin
    # @param    points      A list of matplotlib objects
    # @param    urls        A corresponding list of URLs
    def __init__(self, points, urls):
        self.points = points
        self.urls = urls
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None
        self.dict_ = {"type": "clickinfo",
                      "id": mpld3.utils.get_id(points, suffix),
                      "urls": urls}