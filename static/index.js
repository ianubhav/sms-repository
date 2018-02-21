$(document).ready(function() {

   var search_table = $('#search').DataTable({
      "searching": false,
      "ordering": false,
      "autoWidth": true
      });

    $(function() {
        $('#upload-file-btn').click(function() {
            var file_data = $("#filedata").prop("files")[0];
            var form_data = new FormData();
            form_data.append("json_file", file_data)
            $.ajax({
                type: 'POST',
                url: '/upload',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function(data) {
                  $(".search_table").css("visibility", "visible");
                  search_table.clear().draw()
                  for (var i = 0; i < data.length; i++) {
                      search_table.row.add( [
                        i+1,
                        data[i].sender,
                        data[i].last_digits,
                        data[i].amount,
                        data[i].transaction_time,
                        data[i].sms_timestamp
                    ] ).draw( false );
                  }
                },
            });
        });
    });

    $('input[type=file]').change(function(){
        if($('input[type=file]').val()==''){
            $('button').attr('disabled',true)
        }
        else{
          $('button').attr('disabled',false);
        }
    })


});


