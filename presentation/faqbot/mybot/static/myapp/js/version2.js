(function() {
    var Message; // contains the message object which has all details about the message
    Message = function(arg) {
        this.text = arg.text, this.message_side = arg.message_side,
        this.prompt_feedback = arg.prompt_feedback, this.conversation_key = arg.conversation_key,
        this.feedback_for_question = arg.feedback_for_question,
        this.user_feedback = arg.user_feedback;
        this.draw = function(_this) {
            return function() {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function() {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        this.getQueryString = function(_this) {
            return function() {
                if (_this.feedback_for_question !== ''){
                    return '?feedback=' + _this.user_feedback + '&conversation_key' + _this.conversation_key;
                } else {
                    return '';
                }
            };
        }(this);
        this.reset = function(_this) {
            return function() {
                _this.prompt_feedback = ''
                _this.conversation_key = ''
                _this.feedback_for_question = ''
            };
        }(this);
        this.isFeedBack = function(_this) {
            return function() {
                _this.feedback_for_question !== ''
            };
        }(this);
        return this;
    };
    $(function() {
        var getMessageText, message_side, sendMessage, message;
        message = new Message({ // initialize once globally
                text: 'Hello Welcome !!! I am FAQ BOT .. How can I help you ?',
                message_side: 'right',
                prompt_feedback: '',
                conversation_key: '',
                feedback_for_question: ''
            });

        getMessageText = function() {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        callApi = function(message){
            question = message.isFeedBack() ? message.feedback_for_question : message.text;
            query_string = message.getQueryString();
            $.ajax({
                url: 'http://localhost:9080/bot/dev-ops/' + question + query_string,
                type: 'GET',
                cache: false,
                processData: false,
                contentType: false,
                success: function(data, question) {
                    console.log(data);
                    processMessage(data, question);
                }
            });
        };
        processMessage = function(data, question) {
            if (data === '' || data === undefined) {
                return;
            }
            message.text = data.answer;
            if (message.prompt_feedback == 'Y'){
                message.prompt_feedback = data.prompt_feedback;
                message.conversation_key = data.conversation_key;
                message.feedback_for_question = question;
                message.text = message.text + '\n Is this the answer you are looking for? Please reply "yes" or "no". To abort, reply "stop".'
            }
            sendMessage(message);
        };
        sendMessage = function(message) {
            var $messages;
            if (message === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message.message_side = message.message_side === 'left' ? 'right' : 'left';
            message.draw();
            return $messages.animate({
                scrollTop: $messages.prop('scrollHeight')
            }, 300);
        };
        $('.send_message').click(function(e) {
            return processUserInput();
        });
        $('.message_input').keyup(function(e) {
            if (e.which === 13) {
                return processUserInput();
            }
        });
        processUserInput = function (){
            message.text = getMessageText();
            sendMessage(message);
            return callApi(message);
        };
        sendMessage(message);
    });
}.call(this));