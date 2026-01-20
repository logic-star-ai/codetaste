# Refactor game states into Scene architecture

Introduce `Scene` abstraction to replace fragmented game state logic. Implements `IntroScene`, `TitleScene`, and `GameScene` as concrete scene types, managed through `Context`.