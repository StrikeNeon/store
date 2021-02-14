window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        var t_href = event.target;
        console.log(t_href.name);  // ID корзины
        console.log(t_href.value); // кол-во товаров
        $.ajax({
            url: "/add/" + t_href.name + "/" + t_href.value + "/",
                
            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });

        event.preventDefault();
    });   
}

window.onload = function () {
    $('.basket_list').on('click', 'button[class="btn btn-round"]', function () {
        var t_href = event.target;
        console.log(t_href.name);  // ID корзины
        console.log(t_href.value); // кол-во товаров
        $.ajax({
            url: "/cart_remove/" + t_href.name + "/",
                
            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });

        event.preventDefault();
    });   
}