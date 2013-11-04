var app = app||{}
var ENTER_KEY = 13

//模型
var BookModel = Backbone.Model.extend({});

var BookCollection = Backbone.Collection.extend({

    model: BookModel,

    parse: function(response) {

        return response.books

    }

});


//视图
var BookView = Backbone.View.extend({

    template: _.template( $("#tpl-book-item").html() ),

    contribute_template: _.template( $("#tpl-contribute-form").html() ),

    className: "well row-fluid",

    events: {
        "click .btn-want": "want",
        "click .have": 'have'
    },

    initialize: function(){
       this.listenTo(this.model, 'destory', this.remove);
       this.listenTo(this.model, 'change', this.render);
    },

    render: function(){

       this.$el.html( this.template( this.model.toJSON() ) );
       return this;

    },

    remove: function(){
        alert("")
    },

    clear: function(){
        this.model.destory();
    },

    want: function(){

         var id = this.model.get('id');
         $.ajax({
              type:"post",
              url:"/api/want/"+id,
              data : this.model.toJSON(),
              success:function(result,statusText,jqXHR){
                  $("#alert-ilike-success").show(1000);
                  setTimeout(function(){
                    $("#alert-ilike-success").hide().remove();
                  },2000)
              },
              error:function(error,jqXHR){
                 $("#alert-error").show(1000);
                  setTimeout(function(){
                    $("#alert-error").hide(1000);
                  },2000)
              }
         });

    },

    have: function(){

        $("#form-contribute").html( this.contribute_template(this.model.toJSON()) );

    }

});

var SearchInputView = Backbone.View.extend({

    el: $("#form-search"),
    template: _.template( $("#tpl-search-input").html() ),
    events: {
        "keypress #txt_key": "searchOnEnter",
        "click button": "doSearch"
    },
    initialize: function(){

        this.$input = $("#txt_key");
        this.listenTo(app.books, 'add', this.addOne);
        this.listenTo(app.books, 'reset', this.addAll);

    },
    render: function(){
        this.$el.html( this.template() );
    },
    addOne: function(model){

       /* console.log('handle app.books add event', model);*/
        var bookView = new BookView({model:model});
        var el = bookView.render().el;
        $("#books").append(el);

    },
    searchOnEnter: function(event){

         if(event.which !==ENTER_KEY){
            return;
         }
         this.doSearch(event);

    },
    doSearch: function( event ){

        var keyword = $("#txt_key").val().trim();
        if(keyword){
            $("#ajax_message").fadeIn(500);

            Backbone.ajax({
                type:"get",
                contentType:'application/json',
                url:"/api/book/search/"+keyword+"?fields=id,title,publisher,author,isbn13,image,images",
                timeout:1000000,
                success:function(result,textStatus, jqXHR){

                    app.books.remove(app.books.slice(0));
                    $("#ajax_message").fadeOut(400);
                    $("#books").empty();
                    books = $.parseJSON(result).books;
                    for(var index in books){

                        var bookModel = new BookModel().parse(books[index]);
                        app.books.add(bookModel);

                    }

                },
                error:function(jqXHR,textStatus,errorThrown){
                    console.log(textStatus);
                }
            });


        }

    }

});



$(function(){

    app.books = new BookCollection();
    app.searchInputView = new SearchInputView().render();
    $("#contribute-submit").click(function(){
        $("#form-contribute").submit();
    });

});

