$(document).ready(function () {
    $('#dock_results_list_table').DataTable({
        order: [[2, 'desc']]
    });

    // $('a.editor_create').on('click', function (e) {
    //     e.preventDefault();
    //
    //     editor.create( {
    //         title: 'Create new record',
    //         buttons: 'Add'
    //     } );
    // } );

    $('#dock_results_list_container #delete_jobs').on('click', function(){
        var values = new Array();
        $.each($('#dock_results_list_table .job-results-check-box:checked'), function(){
            values.push($(this).val());
        });
        $.ajax({
            type : "DELETE",
            url : "/results/delete_jobs",
            data: JSON.stringify(values),
            contentType: 'application/json',
            success: function(result){
                // alert("Success !" +result);
                var table = $('#dock_results_list_table')
                table.ajax.reload();
                // $('#dock_results_list_table').ajax.reload();
                // $('#dock_results_list_table').each(function() {
                //     dt = $(this).dataTable();
                //     dt.fnDraw();
                // });
            },
            error: function(error){
                // alert("Error! " + error.text());
            }
        });

    });
});
