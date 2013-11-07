/**
 * Created by zheng on 13-11-7.
 */
var app = app || {}

var IndexView = Backbone.View.extend({

    template: _.template( $('#tpl_index').html() ),

    initialize: function(){

    },

    render: function(){

        this.$el.html( this.template() )
        return this;
    }

});

var AppView = Backbone.View.extend({

    el: 'body',

    initialize: function(){

        this.on('navigate', this.navigate);

    },

    navigate: function(url){

        console.log(url);
       

    },

    navigate_to_index: function(){
        var indexView = new IndexView();
        console.log( indexView.render().el );
    }

});

app.appView = new AppView();

