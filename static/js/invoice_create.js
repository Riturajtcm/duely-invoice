$(document).ready(function() {
	var invoice_form_prefix="invoice_items";

    $('.invoice_item_form_set').formset({
        deleteText: 'del',
        prefix:invoice_form_prefix,
        deleteCssClass:' btn btn-link ',
        addCssClass:' btn btn-link add-row',
        addText:'more',
        formCssClass:'formset_row',
        deleteCallback:function(){ 
        	var total_form = $("#id_"+invoice_form_prefix+"-TOTAL_FORMS").val();
        	if (total_form <= 1){
        		alert("Need at least one form ")
        		$( "a.add-row" ).trigger( "click" );
        	register_event_handles()
        	}
        	setTimeout(function(){ 
                register_event_handles()
        	    calculate_prices()
        	 }, 500);
        	
        	
        },
        added: function(){
               register_event_handles()
            },
    });

    $(".invoice_item_price_total").each(function(){
            $(this).prop("readonly", true);
    })

    function  calculate_prices(){
    	var total_form = $("#id_"+invoice_form_prefix+"-TOTAL_FORMS").val();
    	var over_total_price = 0;
    	for(i=0 ;  i<total_form; i ++){
                var row_unit_quantity = $("#id_"+invoice_form_prefix+"-"+i+"-quantity").val();
                var row_unit_price = $("#id_"+invoice_form_prefix+"-"+i+"-unit_price").val();
                var row_total = row_unit_quantity * row_unit_price;

                $("#id_"+invoice_form_prefix+"-"+i+"-price").val(row_total);
                over_total_price = over_total_price + row_total;

    	}

    	$("#invoice_total_price").text(over_total_price);
    }

    function register_event_handles(){
    	$(".invoice_item_price_total").each(function(){
            $(this).prop("readonly", true);
        })

        $( ".invoice_item_quantity" ).each(function(index) {
		    $(this).on("change", function(){
		           calculate_prices()
		    });
		});

		$( ".invoice_item_unit_price" ).each(function(index) {
		    $(this).on("change", function(){
		           calculate_prices()
		    });
		});

    }

    // register

    register_event_handles()

    
});