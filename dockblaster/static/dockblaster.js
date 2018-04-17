$(document).ready(function () {
    $('#dock_results_list_table').DataTable({
        order: [[1, 'desc']]
    });

    // $('a.editor_create').on('click', function (e) {
    //     e.preventDefault();
    //
    //     editor.create( {
    //         title: 'Create new record',
    //         buttons: 'Add'
    //     } );
    // } );

    $('#dock_results_list_table .job-results-check-box').on('click', function(){
        if($(this).is(':checked')){
            // alert("Checked !");
            // $(this).removeClass('selected');
        }
        else{
            // alert("Unchecked !");
        //     table.$('tr.selected').removeClass('selected');
        //     $(this).addClass('selected');
        }
    });

    $('#dock_results_list_container #delete_jobs').on('click', function(){
        var values = new Array();
        $.each($('#dock_results_list_table .job-results-check-box:checked'), function(){
            values.push($(this).val());
        });
        $.ajax({
            type : "DELETE",
            url : "/delete_jobs",
            data: values,
            contentType: 'application/json;charset=UTF-8',
            success: function(result){
                alert("Success !" +result);
            },
            error: function(error){
                // alert("Error! " + error.text());
            }
        });

    });
});
