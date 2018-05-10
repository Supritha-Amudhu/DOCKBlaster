$(document).ready(function () {
    var dock_results_table = $('#dock_results_list_table').DataTable({
        order: [[2, 'desc']]
    });

    $('#dock_results_list_container #delete_jobs').on('click', function(){
        var values = new Array();
        $.each($('#dock_results_list_table .job-results-check-box:checked'), function(){
            values.push($(this).val());
        });
        $.ajax({
            type : "DELETE",
            url : "/results/delete_jobs",
            data: JSON.stringify(values),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(result){
                console.log(result);
                $.each( result, function( key, value ) {
                    $('#dock_results_list_table .job-results-check-box:checked').each(function(index,obj){
                       if($(obj).attr('id').contains("_"+key) && value == true) {
                           var tableRow = $(obj).closest('tr');
                           console.log("Deleting "+$(tableRow).attr('id'));
                            dock_results_table.row(tableRow).remove().draw();
                       }
                    });
                });
            },
            error: function(error){
                alert("Error! " + error);
            }
        });
    });
    $('[data-toggle="popover"]').popover({content: dockblaster.getFileContents});
    $('[data-toggle="tooltip"]').tooltip();
});

var dockblaster = {
    getFileContents: function(){
        var url = $(this).attr('data-href');
        var preview_text = $.ajax({
            type: "GET",
            url: url,
            async: false
        }).responseText.substring(0,200);
        if(preview_text.length == 0){
            preview_text = "File empty.";
        }
        return preview_text;
    }
}