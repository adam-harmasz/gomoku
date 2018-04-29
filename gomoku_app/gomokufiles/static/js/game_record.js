
    $(document).ready(function () {

        var turn = 'O',
            move = 0,
            grid_coordinates = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o'];
        console.log(context);

        // {#Creating board#}
        function board() {
            var board_div = $('.board-container');
            for (var j = 0; j < 15; j++) {
                var new_div_row = $('<div class="col-master ' + grid_coordinates[j] + '">' + grid_coordinates[j] + '</div>');
                $(board_div.append(new_div_row));
                for (var i = 0; i < 15; i++) {
                    var new_div_col = $('<div class="col-slave ' +
                        grid_coordinates[j] +
                        ' ' + (i + 1) + '"' + '' +
                        ' name="E"></div>');
                    $(new_div_row.append(new_div_col));
                }
            }
        }

        // {#Adding move on board from game record which is imported from Django back-end as context#}
        function nextMove() {
            var searchDiv = $('.next'),
                nextDiv = '';
            if( move < 256) {
                searchDiv.on('click', function () {
                    turn = turn === 'O' ? 'X' : 'O';
                    console.log(context[move][0] + context[move][1]);
                    console.log(nextDiv.className + 'CO ZNALAZŁEM');
                    console.log(move + 'KTÓRY RUCH');
                    $('.' + context[move][0] + '.' + context[move][1] + '').html(turn);
                    move += 1;
                });
            }
        }

        // {#Creating function to undo moves#}
        function prevMove() {
            var searchDiv = $('.prev');
            if( move < 256) {
                searchDiv.on('click', function () {
                    turn = turn === 'O' ? 'X' : 'O';
                    move -= 1;
                    $('.' + context[move][0] + '.' + context[move][1] + '').html('');

                });
            }

        }

        // {#function responsible for starting review#}
        function initGame() {
            var start = $('.start');
            start.one('click', function () {
                nextMove();
                prevMove();
                console.log('start!');
                adjustPlayerColor();
                moveGameRecord();
            })
        }

        // {#Players can change their colors after opening, #}
        // {#    so checking if that happened in Game its checked in Django and imported as context with value yes or no#}
        function adjustPlayerColor() {
            console.log(colorSwap + '   testtetstetr');
            if (colorSwap == 'yes') {
                $('.player1').html('O');
                $('.player2').html('X');
            }
            else {
                $('.player1').html('X');
                $('.player2').html('O');
            }
        }

        // {#Creating game record visible on the right side of board#}
        function gameRecord() {
            var divGameRecord = $('.game-record');
            console.log(divGameRecord);
            console.log(context[0] + context[1]);
            for (var i = 0; i < parseInt(context.length, 10); i++) {
                var newDivGameRecord = $('<li class="game-record-slave" name="' + (i + 1) + '">' + (i + 1) + ': ' + context[i].join('') + '</li>');
                    $(divGameRecord.append(newDivGameRecord));
                    console.log('test robienia divów')
            }
        }

        // {#function responsible for clearing board, and reseting turn and move value so we can start from the beginning#}
        function boardClear() {
            var divBoardSlave = $('.col-slave'),
                clearButton = $('.board-clear');
            clearButton.on('click', function () {
                divBoardSlave.html('');
                turn = 'O';
                move = 0;
            })
        }

        // {#Adding event to game-record spans so we can click on specific move and see add moves to that point#}
        function moveGameRecord() {
            var divBoardSlave = $('.col-slave'),
                gameRecordDivs = $('.game-record-slave');
            gameRecordDivs.on('click', function () {
                divBoardSlave.html('');
                turn = 'O';
                move = 0;
                for (var i = 0; i < parseInt($(this).attr('name'), 10); i++){
                    turn = turn === 'O' ? 'X' : 'O';
                    $('.' + context[i][0] + '.' + context[i][1] + '').html(turn);
                    move += 1;
                }
            });
        }

        board();
        initGame();
        gameRecord();
        boardClear();

    });

