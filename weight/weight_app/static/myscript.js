$(document).ready( ()=> {

    console.log('i am alive!')

    $('#health').on('click' , () => {
        $.get('/health' , (data,status)=> {
            $('#text-info').text(data)
        })
    })
});
