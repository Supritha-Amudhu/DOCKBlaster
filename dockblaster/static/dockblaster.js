$(document).ready(function () {
    $('#dock_results_list_table').DataTable({
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
                    if($('#dock_results_list_table .job-results-check-box:checked').attr('id').includes("_"+key)){
                        if(value == true){
                             var row = $('#dock_results_list_table .job-results-check-box:checked').closest('tr').attr('id')
                             $("#"+row).remove();
                        }
                    }
                });
            },
            error: function(error){
                alert("Error! " + error);
            }
        });

    });
});
