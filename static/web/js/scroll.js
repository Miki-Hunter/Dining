var scrolltotop={
    setting: {startline:200, scrollto: 0, scrollduration:1000, fadeduration:[800, 500]},
    controlHTML: '<img src="scroll.png" style="width:50px; height:50px" />',
    controlattrs: {offsetx:20, offsety:75},
    anchorkeyword: '#top', //Enter href value of HTML anchors on the page that should also act as "Scroll Up" links

    state: {isvisible:false, shouldvisible:false},

    scrollup:function(){
        if (!this.cssfixedsupport) //if control is positioned using JavaScript
            this.$control.css({opacity:0}) //hide control immediately after clicking it
        var dest=isNaN(this.setting.scrollto)? this.setting.scrollto : parseInt(this.setting.scrollto)
        if (typeof dest=="string" && jQuery('#'+dest).length==1) //check element set by string exists
            dest=jQuery('#'+dest).offset().top
        else
            dest=0
        this.$body.animate({scrollTop: dest}, this.setting.scrollduration);
    },

    keepfixed:function(){
        var $window=jQuery(window)
        var controlx=$window.scrollLeft() + $window.width() - this.$control.width() - this.controlattrs.offsetx
        var controly=$window.scrollTop() + $window.height() - this.$control.height() - this.controlattrs.offsety
        this.$control.css({left:controlx+'px', top:controly+'px'})
    },

    togglecontrol:function(){
        var scrolltop=jQuery(window).scrollTop()
        if (!this.cssfixedsupport)
            this.keepfixed()
        this.state.shouldvisible=(scrolltop>=this.setting.startline)? true : false
        if (this.state.shouldvisible && !this.state.isvisible){
            this.$control.stop().animate({opacity:0.5}, this.setting.fadeduration[0])
            this.state.isvisible=true
        }
        else if (this.state.shouldvisible==false && this.state.isvisible){
            this.$control.stop().animate({opacity:0}, this.setting.fadeduration[1])
            this.state.isvisible=false
        }
    },


    init:function(){
        jQuery(document).ready(function($){
            var mainobj=scrolltotop
            var iebrws=document.all
            mainobj.cssfixedsupport=!iebrws || iebrws && document.compatMode=="CSS1Compat" && window.XMLHttpRequest
            mainobj.$body=(window.opera)? (document.compatMode=="CSS1Compat"? $('html') : $('body')) : $('html,body')
            mainobj.$control=$('<div id="topcontrol">'+ controlHTML +'</div>')
                .css({position:mainobj.cssfixedsupport? 'fixed' : 'absolute', bottom:mainobj.controlattrs.offsety, right:mainobj.controlattrs.offsetx, opacity:0, cursor:'pointer'})
                .attr({title:'Scroll to Top'})
                .mouseenter(function() { $(this).css("opacity", "1");})
                .mouseleave(function() { $(this).css("opacity", "0.5");})
                .click(function(){mainobj.scrollup(); return false})
                .appendTo('body')
            if (document.all && !window.XMLHttpRequest && mainobj.$control.text()!='')
                mainobj.$control.css({width:mainobj.$control.width()})
            mainobj.togglecontrol()
            $('a[href="' + mainobj.anchorkeyword +'"]').click(function(){
                mainobj.scrollup()
                return false
            })
            $(window).bind('scroll resize', function(e){
                mainobj.togglecontrol()
            })
        })
    }
}
scrolltotop.init()

