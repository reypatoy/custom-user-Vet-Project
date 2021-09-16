$(document).ready(function(){
    
    $('#date').datepicker({
        dateFormat:'dd/mm/yy'
    });
    $('#time').timepicker({
        timeFormat: 'h:mm p',
        interval:30,
        minTime: '8',
        maxTime: '4pm',
        startTime: '8',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    
    });
})