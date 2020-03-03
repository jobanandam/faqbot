function addSpinner(){
    var spinnerHtml = $($('#spinner').clone().html());
    $('#chat_box_faqbot').append(spinnerHtml);
}

function removeSpinner(){
    $('#chat_box_faqbot').find('.spinner').remove();
}
function getTime(){
    var time = new Date();
    var hr = time.getHours(), min = time.getMinutes(), ampm;
    hr = (hr > 12) ? (hr - 12) : hr;
    hr = ((hr+"").length) == 1 ? ("0"+hr) : hr;
    ampm = (hr > 12) ? "pm" : "am";
    return hr + ":" + min + " " + ampm;
}

function AddBotChat(text) {
    var botChatHtml = $($('#bot_chat').clone().html());
    botChatHtml.find('.text').html(text);
    botChatHtml.find('.timestamp').html(getTime());
    $('#chat_box_faqbot').append(botChatHtml);
    $("#chat_box_faqbot").animate({ scrollTop: $('#chat_box_faqbot').prop("scrollHeight")}, 1000);
}

function AddHumanChat(text) {
    var humanChatHtml = $($('#human_chat').clone().html());
    humanChatHtml.find('.text').html(text);
    humanChatHtml.find('.timestamp').html(getTime());
    $('#chat_box_faqbot').append(humanChatHtml);
    $("#chat_box_faqbot").animate({ scrollTop: $('#chat_box_faqbot').prop("scrollHeight")}, 1000);
}

function onEnter(){
    var text = $("#btn-input").val();
    $("#btn-input").val("");
    if(text !== "" && text !== undefined){
        AddHumanChat(text);
        addSpinner();
        $.ajax({
                url: 'http://localhost:9080/bot/dev-ops/'+text,
                type: 'GET',
                cache: false,
                processData: false,
                contentType: false,
                success: function(data) {
                    AddBotChat(data);
                    removeSpinner();
                }
        });
    }
}


$(function() {
    AddBotChat("Hello ! I'm your DevOps assistant, How may I help you ?");
    $('.chat_input').keyup(function(e) {
    if (e.which === 13) {
        onEnter();
    }
    });
});


