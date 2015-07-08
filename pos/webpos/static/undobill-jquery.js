function undo_bill(event) {
    var container = "#" + $(this).parents(event.data.hide).attr('id');
    var item_id = $(this).attr('id');
    $.ajax({
           type: "POST",
           url: event.data.url,
           data: { billid: item_id,
                   csrfmiddlewaretoken: event.data.csrf_token
           },
           dataType: "json",
           success: function(json) {
                  $(container).hide();
                  alert(json.message);
            },
            error: function(xhr,errmsg,err) {
                   alert(xhr.status + ": " + xhr.responseText);
            }
      });
      return false; 
}
