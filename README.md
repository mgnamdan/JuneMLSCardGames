# June's Card Games

This project contains two versions of the Blackjack and Go Fish application:

- `Terminal Interface` contains the original text-based application.
- `Visual Interface` contains the PyQt6 desktop application.

Blackjack begins each session with $10.00 USD in chips. After finishing a hand,
the player may wager up to $2.00 through the included `Currency` class.

Run the terminal version:

```powershell
python "Terminal Interface/main.py"
```

Run the visual version:

```powershell
python "Visual Interface/main.py"
```

The visual version requires PyQt6. Dependency details are available in
`Visual Interface/requirements.txt`.
