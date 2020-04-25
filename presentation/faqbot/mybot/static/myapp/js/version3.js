/*
* This version contains better ui for feedback
*/
(function() {
    var Message; // contains the message object which has all details about the message
    Message = function(arg) {
        this.text = arg.text, this.message_side = arg.message_side, this.sender = arg.sender,
        this.prompt_feedback = arg.prompt_feedback, this.conversation_key = arg.conversation_key,
        this.feedback_for_question = arg.feedback_for_question, this.index = arg.index,
        this.user_feedback = arg.user_feedback;
        this.draw = function(_this) {
            return function() {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                if (_this.prompt_feedback == 'Y'){
                    $message.find('.feedbackBtn').addClass('showFeedback');
                }
                $('.messages').append($message);
                return setTimeout(function() {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        this.getQueryString = function(_this) {
            return function() {
                if (_this.feedback_for_question !== ''){
                    return '?feedback=' + _this.user_feedback + '&conversation_key=' + _this.conversation_key + '&index=' + _this.index;
                } else {
                    return '';
                }
            };
        }(this);
        this.clearFeedbackState = function(_this) {
            return function() {
                _this.prompt_feedback = 'N', _this.user_feedback = '', _this.feedback_for_question = '', _this.index = -1;
            };
        }(this);
        this.reset = function(_this) {
            return function() {
                _this.prompt_feedback = ''; _this.user_feedback = ''; _this.conversation_key = '';
                _this.feedback_for_question = ''; _this.index = -1;
            };
        }(this);
        this.isFeedBack = function(_this) {
            return function() {
                return _this.feedback_for_question !== ''
            };
        }(this);
        return this;
    };
    $(function() {
        var getMessageText, message_side, sendMessage, message, sender;
        var state=true;
        message = new Message({ // initialize once globally
                text: 'Hello Welcome, How may I help you ?',
                message_side: 'left',
                sender: 'bot',
                prompt_feedback: '',
                conversation_key: '',
                feedback_for_question: '',
                user_feedback: '',
                index: -1
            });

        getMessageText = function() {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        callApi = function(message){
            question = message.text;
            // add this if you need to treat feedback from textbox
//            message.user_feedback = message.isFeedBack() ? message.text: '';
            query_string = message.getQueryString();
            $.ajax({
                url: 'http://localhost:9080/bot/dev-ops/' + question + query_string,
                type: 'GET',
                cache: false,
                processData: false,
                contentType: false,
                success: function(data) {
                    console.log(data);
                    processMessage(data);
                }
            });
        };
        processMessage = function(data) {
            if (data === '' || data === undefined) {
                return;
            }
            if (data.prompt_feedback == 'Y'){
                message.prompt_feedback = data.prompt_feedback;
                message.index = data.index;
                message.feedback_for_question = message.text;
            } else {
                message.clearFeedbackState();
            }
            message.conversation_key = data.user_id;
            message.text = data.answer;
            message.sender = 'bot';
            sendMessage(message);
        };
        sendMessage = function(message) {
            var $messages;
            if (message === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message.message_side = message.sender === 'bot' ? 'left' : 'right';
            message.draw();
            return $messages.animate({
                scrollTop: $messages.prop('scrollHeight')
            }, 300);
        };
        $('.send_message').click(function(e) {
            message.sender = 'human';
            return processUserInput();
        });
        $('.message_input').keyup(function(e) {
            if (e.which === 13) {
                message.sender = 'human';
                return processUserInput();
            }
        });

        $(document).on('click', ".feedbackBtn .like", function(){
            $(this).parent().find('.dislike').addClass('disabled');
            return processUserFeedback('Y');
        });
        $(document).on('click', ".feedbackBtn .dislike", function(){
            $(this).parent().find('.like').addClass('disabled');
            return processUserFeedback('N');
        });

        $( document ).ready(function() {
            $( "#bt" ).click();
        });

       $( "#bt" ).click(function() {
            if(state) {
                $('#collapseExample').css('display', 'none');
                $('#floatable_pane').css('height', '8%');
                $('#header_pane').css('height', '100%');
                $('#bt').text('+');
                $('#title_txt').css('top', '22%');
            }
            else {
                $('#collapseExample').css('display', 'block');
                $('#floatable_pane').css('height', '84%');  // make sure the same value is used in css
                $('#header_pane').css('height', '10%');
                $('#bt').text('X');
                $('#title_txt').css('top', '2.5%');
            }
            state=!state;
        });
        processUserFeedback = function (feedback){
            message.text = message.feedback_for_question;
            message.user_feedback = feedback;
            return callApi(message);
        };
        processUserInput = function (){
            message.clearFeedbackState();
            message.text = getMessageText();
            sendMessage(message);
            return callApi(message);
        };
        sendMessage(message);

    });
}.call(this));

