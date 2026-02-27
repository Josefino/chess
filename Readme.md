Chess Engine
User Manual
Josef@2026

Introduction
Chess Engine is a fully featured chess application designed both for playing and for testing and analysis. The program supports a complete manual mode, allowing users to set up any position using a FEN string, play moves freely for both sides, step through ideas, and evaluate positions on demand — making it an ideal tool not only for casual games but also for studying tactics, verifying engine behaviour, and debugging chess logic.

The application runs natively on macOS as a standalone .app bundle requiring no installation.

Interface Overview
The window is divided into two panels:
•	Left panel — the chessboard with click-to-move interaction.
•	Right panel — controls, status information, move log, captured pieces, and the chess clock.

ℹ  The board automatically resizes to fit the screen. All coordinates adjust accordingly.

Playing a Game
Moving Pieces
Click a piece to select it — legal destination squares are highlighted. Click a destination square to complete the move. To deselect, click elsewhere on the board.
Pawn promotion is handled automatically — the pawn promotes to a Queen.
AI Opponent
Use the AI Move button to make the engine play a single move for the side to move. Use the AUTO button to let the engine play continuously. STOP halts automatic play.
ℹ  The current move, depth, nodes searched, TT size, and evaluation are displayed above the clock after each AI move.
Undo
The UNDO button takes back the last move. Can be pressed repeatedly to step back through the game.
Reset
RESET returns the board to the starting position and clears all statistics, the transposition table, and the move log.

Manual & Testing Mode
The program is fully designed to support manual testing and position analysis:
•	Use Put FEN to load any position directly — enter a valid FEN string and click Load.
•	Play moves for both White and Black freely, regardless of whose turn it is.
•	Use Best Move to ask the engine for its recommendation without committing to the move — the suggested move is highlighted on the board for 2 seconds.
•	Use AI Move to let the engine play a single move and inspect the evaluation.
•	Set Clock to 0 to disable the clock entirely for untimed analysis.

ℹ  This mode is ideal for verifying engine responses to specific positions, testing tactical puzzles, or stepping through opening lines manually.

Controls Reference
Buttons
AI Move	Engine plays one move for the side currently to move.
AUTO	Engine plays continuously for the active side. Press STOP to halt.
STOP	Stops automatic play.
UNDO	Takes back the last move.
RESET	Returns to starting position, clears stats and transposition table.
Best Move	Calculates and highlights the best move without playing it (2-second highlight).
History	Displays the full move history in the info panel.
Copy FEN	Copies the current position FEN to the clipboard and shows it in the info panel.
Put FEN	Opens a dialog to load a position from a FEN string.

Settings
Depth  + Set	Sets the maximum search depth (1–20). Default: 4.
Time(s) + Set	Sets the maximum thinking time per move in seconds (0.5–300). Default: 5.
Clock  + Set	Sets the chess clock in minutes per side. Enter 0 to disable the clock.

Status Display
The right panel shows the following information at all times:
•	Last move label — displays the most recent move in the format  36. [W] e2e4  or  AI thinking…  while the engine is calculating.
•	Chess clock — shows remaining time for White and Black. Hidden when clock is set to 0.
•	AI stats — depth reached, nodes searched (in MN = mega-nodes), transposition table size, and evaluation in pawns.
•	Move log — scrollable list of game events, check and checkmate announcements.
•	Captured pieces — shows pieces lost by each side, updated after every move.

ℹ  Evaluation is shown from White's perspective: positive values favour White, negative values favour Black.

Mate Detection
After each move, the engine checks for forced mate sequences when the evaluation exceeds 3 pawns advantage. If a forced mate is found, the result is shown in the last move label (e.g.  1. [B] d1h5  ► Mate in 2!) and an audible warning is played.
ℹ  Mate search depth is limited to 6 moves to keep response time fast. Reduce the eval threshold or depth in the source if needed.

Sound Effects
Move	Short two-tone click on every piece move.
Check	Two-tone alert when a king is in check.
Checkmate	Four-note fanfare on checkmate.
Draw	Descending three-note tone on stalemate.
Mate warning	Triple pulse when a forced mate sequence is detected.

ℹ  All sounds are generated internally using WAV synthesis — no external audio files are required.

Terminal Commands
The program also accepts commands typed in the terminal window from which it was launched:
e2e4	Play the move e2-e4 (UCI format).
best	Show the best move without playing it.
h / history	Print the move history.
b / back	Undo the last move.
fen	Print the current FEN.
dep N	Set search depth to N.
lim N	Set time limit to N seconds.
go	Start AUTO mode.
stop	Stop AUTO mode.
q	Quit the application.

System Requirements
•	macOS 10.13 (High Sierra) or later.
•	Apple Silicon (arm64) and Intel (x86_64) supported.
•	No installation required — run directly from the .app bundle.

If running from source: Python 3.9+, python-chess, and tkinter are required.

<img width="468" height="647" alt="image" src="https://github.com/user-attachments/assets/7203887b-2c0a-4b53-b815-f32559ef1271" />
