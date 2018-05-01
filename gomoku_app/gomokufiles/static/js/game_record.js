
    $(document).ready(function () {

        var /*$black_stone = $('#black_stone').append(),
            $white_stone = $('#white_stone').append(),*/
            turn = 'O',
            move = 0,
            grid_coordinates = ['o/x', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o'];
        console.log(white_img);

        // {#Creating board#}
        function board() {
            var board_div = $('.board-container');
            for (var j = 0; j < 16; j++) {
                var new_div_row = $('<div class="col-master ' + grid_coordinates[j]
                    + '"' + ' id="coord-' + j + '"' + '>' + grid_coordinates[j] + '</div>');
                $(board_div.append(new_div_row));
                if (j === 0){
                    for (var k = 0; k < 15; k++) {
                        var numberCoordEl = $('<div class="board-coord"><span class="board-coord-slave">'
                            + (k + 1) +'</span></div>');
                        new_div_row.append(numberCoordEl);
                    }
                } else {
                    for (var i = 0; i < 15; i++) {
                        var new_div_col = $('<div class="col-slave ' +
                            grid_coordinates[j] +
                            ' ' + (i + 1) + '"' + '></div>');
                        $(new_div_row.append(new_div_col));
                    }
                }
            }
        }


        // {#Adding move on board from game record which is imported from Django back-end as context#}
        function nextMove() {
            var search_div = $('.next');

            search_div.on('click', function (event) {
                event.preventDefault();
                console.log(move + " który ruch");
                turn = turn === 'O' ? 'X' : 'O';
                console.log(context[move][0] + context[move][1]);
                console.log(move + 'KTÓRY RUCH');
                if (turn === 'O') {
                    $('.' + context[move][0] + '.' + context[move][1] + '').html($('<img src="' + white_src + '">'));
                    move += 1;
                    if (move === 1) {
                        prevMove();
                    } else if (move >= context.length) {
                        silenceNext();
                    }
                } else {
                    $('.' + context[move][0] + '.' + context[move][1] + '').html($('<img src="' + black_src + '">'));
                    move += 1;
                    if (move === 1) {
                        prevMove();
                    } else if (move >= context.length) {
                        silenceNext();
                    }
                }
            })
        }

        function silenceNext() {
            $('.next').off('click');
        }

        // {#Creating function to undo moves#}
        function prevMove() {
            var search_div = $('.prev');

            search_div.on('click', function (event) {
                event.preventDefault();
                turn = turn === 'O' ? 'X' : 'O';
                if (move === context.length) {
                    silenceNext();
                    nextMove();
                    silenceLast();
                    lastMove();
                }
                move -= 1;
                $('.' + context[move][0] + '.' + context[move][1] + '').html('');
                if (move === 0) {
                    silencePrev();
                    silenceLast();
                    lastMove();
                }
            });
        }

        function silencePrev() {
            $('.prev').off('click');
        }

        //Added a button which will show load on board whole game
        function lastMove() {
            var last_button = $('.last'),
                board_slave = $('.col-slave');

            last_button.on('click', function (event) {
                event.preventDefault();
                board_slave.html('');
                turn = 'O';
                move = 0;
                for (var i = 0; i < context.length; i++){
                    turn = turn === 'O' ? 'X' : 'O';
                    if (turn === 'O') {
                        $('.' + context[i][0] + '.' + context[i][1] + '').html($('<img src="' + white_src + '">'));
                        move += 1;
                    } else {
                        $('.' + context[i][0] + '.' + context[i][1] + '').html($('<img src="' + black_src + '">'));
                        move += 1;
                    }
                }
                console.log(move + "  który mamy ruch");
                silencePrev();
                prevMove();
                silenceNext();
                silenceLast();
            });
        }

        function silenceLast() {
            $('.last').off('click');
        }

        // {#function responsible for starting review#}
        function initGame() {
            var start = $('.start');
            start.one('click', function (event) {
                event.preventDefault();
                nextMove();
                lastMove();
                console.log('start!');
                adjustPlayerColor();
                moveGameRecord();
            })
        }

        // {#Players can change their colors after opening, #}
        // {#    so checking if that happened in Game its checked in Django and imported as context with value yes or no#}
        function adjustPlayerColor() {
            console.log(colorSwap + '   testtetstetr');
            if (colorSwap === 'yes') {
                $('.player1').html(white_img);
                $('.player2').html(black_img);
            }
            else {
                $('.player1').html(black_img);
                $('.player2').html(white_img);
            }
        }

        // {#Creating game record visible on the right side of board#}
        function gameRecord() {
            var divGameRecord = $('.game-record');
            console.log(divGameRecord);
            console.log(context[0] + context[1]);

            for (var i = 0; i < parseInt(context.length, 10); i++) {
                var newDivGameRecord = $('<button class="game-record-slave" name="' + (i + 1) + '">' + (i + 1) + ': ' + context[i].join('') + '</button>');
                    $(divGameRecord.append(newDivGameRecord));

                if ((i + 1) === context.length) {
                    console.log('test silenca');
                    newDivGameRecord.on('click', function () {
                        silenceNext();
                        silencePrev();
                        prevMove();
                    });
                }
            }
        }

        // {#function responsible for clearing board, and reseting turn and move value so we can start from the beginning#}
        function boardClear() {
            var divBoardSlave = $('.col-slave'),
                clearButton = $('.board-clear');

            clearButton.on('click', function (event) {
                event.preventDefault();
                divBoardSlave.html('');
                turn = 'O';
                move = 0;
                silenceNext();
                silencePrev();
                nextMove();
            })
        }

        // {#Adding event to game-record spans so we can click on specific move and see add moves to that point#}
        function moveGameRecord() {
            var divBoardSlave = $('.col-slave'),
                gameRecordDivs = $('.game-record-slave');

            gameRecordDivs.on('click', function (event) {
                event.preventDefault();

                divBoardSlave.html('');
                turn = 'O';
                move = 0;
                for (var i = 0; i < parseInt($(this).attr('name'), 10); i++){
                    turn = turn === 'O' ? 'X' : 'O';
                    if (turn === 'O') {
                        $('.' + context[i][0] + '.' + context[i][1] + '').html($('<img src="' + white_src + '">'));
                        move += 1;
                    } else {
                        $('.' + context[i][0] + '.' + context[i][1] + '').html($('<img src="' + black_src + '">'));
                        move += 1;
                    }
                    if (move === context.length) {
                        silenceLast();
                    } else {
                        lastMove();
                    }
                }
                silencePrev();
                prevMove();
            });
        }

        board();
        initGame();
        gameRecord();
        boardClear();

    });

