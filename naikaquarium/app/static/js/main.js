$('.add-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log(id);
    $.ajax({
        type: "GET",
        url: '/add_cart',
        data: {
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }
    })
})



$('.subtract-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log(id);
    $.ajax({
        type: "GET",
        url: '/subtract_cart',
        data: {
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }
    })
})

$('.delete-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    console.log(id);
    $.ajax({
        type: "GET",
        url: '/delete_cart',
        data: {
            prod_id: id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
    location.reload();
})
