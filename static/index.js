$(document).ready(function(){

    $("#toggle-video").click(function(){
    var imgDiv = $('.panel-1-left');
        if (imgDiv.style.display !== 'none') {
        imgDiv.style.display = 'none';
    }
    else {
        imgDiv.style.display = 'block';
    }

    })

    var postArgOnClick = function(selector, endpoint, arg){
    return $(selector).click(function(){
        $.post(endpoint, {arg})
    })
    } 

    var postOnClick = function(selector,endpoint){
    return $(selector).click(function(){
        $.post(endpoint, {})
    })
    } 

    var moveMotorOnPress = function(selector, arg){
    return $(selector).on('mousedown touchstart', function(e) {
        $(this).addClass('active-btn');
        $.post('/move', {arg})
    })
    .bind('mouseup mouseleave touchend', function() {
    $(this).removeClass('active');
    $.post('/move', {arg:"STOP"})
    });
    }

    var moveServoOnPress = function(selector, arg){
    return $(selector).on('mousedown touchstart', function(e) {
        $(this).addClass('active-btn');
        timeOut = setInterval(function(){
        $.post('/servo', {arg})}, 100 )
    })
    .bind('mouseup mouseleave touchend', function() {
    $(this).removeClass('active');
    clearInterval(timeOut);

    });
    }

    window.setInterval(function(){
        while (1){
        $.get('/battery_percentage', function(data){
            $("#battery-percentage").html(data);
        });
        }}, 5000);

    // test endpoints
    postArgOnClick('#testLEDs', '/test', 'Led');
    postArgOnClick('#testMotors', '/test', 'Motor');
    postArgOnClick('#testUltrasonic', '/test', 'Ultrasonic');
    postArgOnClick('#testInfrared', '/test', 'Infrared');
    postArgOnClick('#testServo', '/test', 'Servo');
    postArgOnClick('#testADC', '/test', 'ADC');
    postArgOnClick('#testBuzzer', '/test', 'Buzzer');
    postArgOnClick('#testAll', '/test', 'ALL');

    postOnClick("#line-tracking-btn", "/line_tracking");
    postOnClick("#line-following-btn", "/line_following");
    postOnClick("#person-tracking-btn", "/person_tracking");
    postOnClick("#ultrasonic-tracking-btn", "/ultrasonic_tracking");
    postOnClick("#light-tracking-btn", "/light_tracking");

    moveMotorOnPress("#motor-forward-btn", "FORWARD");
    moveMotorOnPress("#motor-backwards-btn", "BACKWARDS");
    moveMotorOnPress("#motor-left-btn", "LEFT");
    moveMotorOnPress("#motor-right-btn", "RIGHT");
    moveMotorOnPress("#motor-stop-btn", "STOP");


    moveServoOnPress("#servo-up-btn", "UP");
    moveServoOnPress("#servo-down-btn", "DOWN");
    moveServoOnPress("#servo-left-btn", "LEFT");
    moveServoOnPress("#servo-right-btn", "RIGHT");
    moveServoOnPress("#servo-home-btn", "HOME");

})