$('.remove_item').click(function(){
    var product_id;
    product_id = $(this).attr("product_id");
    $.ajax(
    {
        type:"POST",
        url: "/cart_remove",
        data:{
            product_id: product_id
        },
        success: function( data ) 
        {
            location.reload();
        }
     })
});