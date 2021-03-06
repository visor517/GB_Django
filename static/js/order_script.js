window.onload = function () {
    let quantity_arr = []
    let price_arr = []

    const TOTAL_FORMS = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',','.')) || 0

    for (let i = 0; i < TOTAL_FORMS; i++) {
        let _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val())
        let _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',','.'))

        quantity_arr[i] = _quantity
        price_arr[i] = _price || 0
    }

    $('.order_form').on('click', 'input[type=number]', function() {
        const orderitem_num = parseInt(event.target.name.replace('orderitems-', '').replace('-quantity', ''))
        if (price_arr[orderitem_num]) {
            let orderitem_quantity = parseInt(event.target.value)
            let delta_quantity = orderitem_quantity - quantity_arr[orderitem_num]
            quantity_arr[orderitem_num] = orderitem_quantity

            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
        }
    })

    $('.order_form').on('click', 'input[type=checkbox]', function() {
        const orderitem_num = parseInt(event.target.name.replace('orderitems-', '').replace('-quantity', ''))

        let delta_quantity = event.target.checked ? -quantity_arr[orderitem_num] : +quantity_arr[orderitem_num]

        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
    })

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        let delta_cost = orderitem_price * delta_quantity

        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2))
        order_total_quantity += delta_quantity

        $('.order_total_quantity').html(order_total_quantity)
        $('.order_total_cost').html(order_total_cost)
    }

    $('.formset_row').formset({
        addText: 'Добавить товар',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    })

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type=number]').name
        let orderitem_num = target_name.replace('orderitems-', '').replace('-quantity', '')
        let delta_quantity = -quantity_arr[orderitem_num]
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
    }

    $('.order_form').on('change', 'select', function () {
        let target = event.target
        const orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''))
        let orderitem_product_pk = target.options[target.selectedIndex].value

        $.ajax({
            url: '/orders/product/' + orderitem_product_pk + '/price/',
            success: function (data) {
                if (data.price) {
                    price_arr[orderitem_num] = parseFloat(data.price)
                    const price_html = '<span>' + String(data.price).replace('.',',') + 'руб.</span>'
                    const curr_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')')
                    curr_tr.find('td:eq(2)').html(price_html)
                    orderSummaryRecalc()
                }
            },
        })
    })

    function orderSummaryRecalc() {
        order_total_quantity = 0
        order_total_cost = 0
        for (let i = 0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i]
            order_total_cost += quantity_arr[i] * price_arr[i]
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }
}