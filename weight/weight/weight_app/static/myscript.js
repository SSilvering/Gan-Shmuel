$(document).ready( ()=> {

    console.log('i am alive!')

    $('#health').on('click' , () => {
        $.get('/health' , (data,status)=> {
            $('#text-info').text(data)
        })
    })

    $('#unknown').on('click' , () => {
        $.get('/unknown' , (data,status)=> {
            $('#text-info').text(data)
            $('#text-info').text(status)
        })
    })
    $('#session').on('click' , () => {
        $.get('/session' , (data,status)=> {
            $('#text-info').text(data)
        })
    })
});
