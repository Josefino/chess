{\rtf1\ansi\ansicpg1250\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Arial-BoldMT;\f1\fswiss\fcharset0 ArialMT;\f2\fswiss\fcharset0 Arial-ItalicMT;
\f3\froman\fcharset0 TimesNewRomanPSMT;\f4\fnil\fcharset0 AppleSymbols;\f5\fmodern\fcharset0 CourierNewPS-BoldMT;
}
{\colortbl;\red255\green255\blue255;\red31\green31\blue31;\red0\green0\blue0;\red119\green72\blue33;
\red117\green117\blue117;\red67\green67\blue67;\red242\green236\blue230;\red193\green193\blue193;}
{\*\expandedcolortbl;;\cssrgb\c16471\c16471\c16471;\cssrgb\c0\c0\c0;\cssrgb\c54510\c35294\c16863;
\cssrgb\c53333\c53333\c53333;\cssrgb\c33333\c33333\c33333;\cssrgb\c96078\c94118\c92157;\cssrgb\c80000\c80000\c80000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\sa160\qc\partightenfactor0

\f0\b\fs74\fsmilli37333 \cf2 \expnd0\expndtw0\kerning0
Chess Engine
\f1\b0\fs29\fsmilli14667 \cf3 \
\pard\pardeftab720\sa106\qc\partightenfactor0

\fs42\fsmilli21333 \cf4 User Manual
\fs29\fsmilli14667 \cf3 \
\pard\pardeftab720\sa640\qc\partightenfactor0

\f2\i \cf5 Josef@2026
\f1\i0 \cf3 \
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Introduction\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 Chess Engine is a fully featured chess application designed both for playing and for testing and analysis. The program supports a complete manual mode, allowing users to set up any position using a FEN string, play moves freely for both sides, step through ideas, and evaluate positions on demand \'97 making it an ideal tool not only for casual games but also for studying tactics, verifying engine behaviour, and debugging chess logic.\
\'a0\
The application runs natively on macOS as a standalone .app bundle requiring no installation.\
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Interface Overview\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 The window is divided into two panels:\
\pard\pardeftab720\li746\fi-374\sa53\partightenfactor0
\cf3 \'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Left panel \'97 the chessboard with click-to-move interaction.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Right panel \'97 controls, status information, move log, captured pieces, and the chess clock.\
\pard\pardeftab720\sa80\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\li533\sa106\partightenfactor0

\f4 \cf4 \uc0\u8505 
\f0\b \'a0 
\f2\i\b0 \cf6 The board automatically resizes to fit the screen. All coordinates adjust accordingly.
\f1\i0 \cf3 \
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Playing a Game\
\pard\pardeftab720\sa160\partightenfactor0

\fs34\fsmilli17333 \cf4 Moving Pieces\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 Click a piece to select it \'97 legal destination squares are highlighted. Click a destination square to complete the move. To deselect, click elsewhere on the board.\
Pawn promotion is handled automatically \'97 the pawn promotes to a Queen.\
\pard\pardeftab720\sa160\partightenfactor0

\f0\b\fs34\fsmilli17333 \cf4 AI Opponent\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 Use the AI Move button to make the engine play a single move for the side to move. Use the AUTO button to let the engine play continuously. STOP halts automatic play.\
\pard\pardeftab720\li533\sa106\partightenfactor0

\f4 \cf4 \uc0\u8505 
\f0\b \'a0 
\f2\i\b0 \cf6 The current move, depth, nodes searched, TT size, and evaluation are displayed above the clock after each AI move.
\f1\i0 \cf3 \
\pard\pardeftab720\sa160\partightenfactor0

\f0\b\fs34\fsmilli17333 \cf4 Undo\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 The UNDO button takes back the last move. Can be pressed repeatedly to step back through the game.\
\pard\pardeftab720\sa160\partightenfactor0

\f0\b\fs34\fsmilli17333 \cf4 Reset\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 RESET returns the board to the starting position and clears all statistics, the transposition table, and the move log.\
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Manual & Testing Mode\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 The program is fully designed to support manual testing and position analysis:\
\pard\pardeftab720\li746\fi-374\sa53\partightenfactor0
\cf3 \'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Use Put FEN to load any position directly \'97 enter a valid FEN string and click Load.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Play moves for both White and Black freely, regardless of whose turn it is.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Use Best Move to ask the engine for its recommendation without committing to the move \'97 the suggested move is highlighted on the board for 2 seconds.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Use AI Move to let the engine play a single move and inspect the evaluation.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Set Clock to 0 to disable the clock entirely for untimed analysis.\
\pard\pardeftab720\sa80\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\li533\sa106\partightenfactor0

\f4 \cf4 \uc0\u8505 
\f0\b \'a0 
\f2\i\b0 \cf6 This mode is ideal for verifying engine responses to specific positions, testing tactical puzzles, or stepping through opening lines manually.
\f1\i0 \cf3 \
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Controls Reference\
\pard\pardeftab720\sa160\partightenfactor0

\fs34\fsmilli17333 \cf4 Buttons\

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrt\brdrnil \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3546\clftsWidth3 \clbrdrt\brdrs\brdrw20\brdrcf8 \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8233\clftsWidth3 \clbrdrt\brdrs\brdrw20\brdrcf8 \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\fs26\fsmilli13333 \cf3 AI Move
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Engine plays one move for the side currently to move.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3546\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8233\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 AUTO
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Engine plays continuously for the active side. Press STOP to halt.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3546\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8233\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 STOP
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Stops automatic play.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3546\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8233\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 UNDO
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Takes back the last move.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3546\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8233\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 RESET
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Returns to starting position, clears stats and transposition table.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3546\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8233\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Best Move
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Calculates and highlights the best move without playing it (2-second highlight).
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3546\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8233\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 History
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Displays the full move history in the info panel.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3546\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8233\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Copy FEN
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Copies the current position FEN to the clipboard and shows it in the info panel.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrt\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3546\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8233\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Put FEN
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Opens a dialog to load a position from a FEN string.
\fs29\fsmilli14667 \cell \lastrow\row
\pard\pardeftab720\sa80\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa160\partightenfactor0

\f0\b\fs34\fsmilli17333 \cf4 Settings\

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrt\brdrnil \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3553\clftsWidth3 \clbrdrt\brdrs\brdrw20\brdrcf8 \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8227\clftsWidth3 \clbrdrt\brdrs\brdrw20\brdrcf8 \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\fs26\fsmilli13333 \cf3 Depth\'a0 + Set
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Sets the maximum search depth (1\'9620). Default: 4.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3553\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8227\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Time(s) + Set
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Sets the maximum thinking time per move in seconds (0.5\'96300). Default: 5.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrt\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3553\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8227\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Clock\'a0 + Set
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Sets the chess clock in minutes per side. Enter 0 to disable the clock.
\fs29\fsmilli14667 \cell \lastrow\row
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Status Display\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 The right panel shows the following information at all times:\
\pard\pardeftab720\li746\fi-374\sa53\partightenfactor0
\cf3 \'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Last move label \'97 displays the most recent move in the format\'a0 36. [W] e2e4\'a0 or\'a0 AI thinking\'85\'a0 while the engine is calculating.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Chess clock \'97 shows remaining time for White and Black. Hidden when clock is set to 0.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 AI stats \'97 depth reached, nodes searched (in MN = mega-nodes), transposition table size, and evaluation in pawns.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Move log \'97 scrollable list of game events, check and checkmate announcements.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Captured pieces \'97 shows pieces lost by each side, updated after every move.\
\pard\pardeftab720\sa80\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\li533\sa106\partightenfactor0

\f4 \cf4 \uc0\u8505 
\f0\b \'a0 
\f2\i\b0 \cf6 Evaluation is shown from White's perspective: positive values favour White, negative values favour Black.
\f1\i0 \cf3 \
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Mate Detection\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 After each move, the engine checks for forced mate sequences when the evaluation exceeds 3 pawns advantage. If a forced mate is found, the result is shown in the last move label (e.g.\'a0 1. [B] d1h5\'a0 \uc0\u9658  Mate in 2!) and an audible warning is played.\
\pard\pardeftab720\li533\sa106\partightenfactor0

\f4 \cf4 \uc0\u8505 
\f0\b \'a0 
\f2\i\b0 \cf6 Mate search depth is limited to 6 moves to keep response time fast. Reduce the eval threshold or depth in the source if needed.
\f1\i0 \cf3 \
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Sound Effects\

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrt\brdrnil \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3565\clftsWidth3 \clbrdrt\brdrs\brdrw20\brdrcf8 \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8215\clftsWidth3 \clbrdrt\brdrs\brdrw20\brdrcf8 \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\fs26\fsmilli13333 \cf3 Move
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Short two-tone click on every piece move.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3565\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8215\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Check
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Two-tone alert when a king is in check.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3565\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8215\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Checkmate
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Four-note fanfare on checkmate.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3565\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8215\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Draw
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Descending three-note tone on stalemate.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrt\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3565\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8215\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 Mate warning
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Triple pulse when a forced mate sequence is detected.
\fs29\fsmilli14667 \cell \lastrow\row
\pard\pardeftab720\sa80\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\li533\sa106\partightenfactor0

\f4 \cf4 \uc0\u8505 
\f0\b \'a0 
\f2\i\b0 \cf6 All sounds are generated internally using WAV synthesis \'97 no external audio files are required.
\f1\i0 \cf3 \
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 Terminal Commands\
\pard\pardeftab720\sa80\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 The program also accepts commands typed in the terminal window from which it was launched:\

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrt\brdrnil \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3549\clftsWidth3 \clbrdrt\brdrs\brdrw20\brdrcf8 \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8230\clftsWidth3 \clbrdrt\brdrs\brdrw20\brdrcf8 \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 e2e4
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Play the move e2-e4 (UCI format).
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 best
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Show the best move without playing it.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 h / history
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Print the move history.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 b / back
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Undo the last move.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 fen
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Print the current FEN.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 dep N
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Set search depth to N.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 lim N
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Set time limit to N seconds.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 go
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Start AUTO mode.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalt \clcbpat7 \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clcbpat7 \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 stop
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Stop AUTO mode.
\fs29\fsmilli14667 \cell \row

\itap1\trowd \taflags1 \trgaph108\trleft-108 \trwWidth12480\trftsWidth3 \trbrdrl\brdrnil \trbrdrt\brdrnil \trbrdrr\brdrnil 
\clvertalt \clshdrawnil \clwWidth3549\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrs\brdrw20\brdrcf8 \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx4320
\clvertalt \clshdrawnil \clwWidth8230\clftsWidth3 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrs\brdrw20\brdrcf8 \clbrdrr\brdrs\brdrw20\brdrcf8 \clpadt106 \clpadl160 \clpadb106 \clpadr160 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f5\b\fs26\fsmilli13333 \cf3 q
\f1\b0\fs29\fsmilli14667 \cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0

\fs26\fsmilli13333 \cf3 Quit the application.
\fs29\fsmilli14667 \cell \lastrow\row
\pard\pardeftab720\sa213\partightenfactor0
\cf3 \'a0\
\pard\pardeftab720\sa213\partightenfactor0

\f0\b\fs42\fsmilli21333 \cf2 System Requirements\
\pard\pardeftab720\li746\fi-374\sa53\partightenfactor0

\f1\b0\fs29\fsmilli14667 \cf3 \'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 macOS 10.13 (High Sierra) or later.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 Apple Silicon (arm64) and Intel (x86_64) supported.\
\'95
\f3\fs18\fsmilli9333 \'a0\'a0\'a0\'a0 
\f1\fs29\fsmilli14667 No installation required \'97 run directly from the .app bundle.\
\pard\pardeftab720\sa80\partightenfactor0
\cf3 \'a0\
If running from source: Python 3.9+, python-chess, and tkinter are required.\
\pard\pardeftab720\partightenfactor0
\cf3 \'a0\
}