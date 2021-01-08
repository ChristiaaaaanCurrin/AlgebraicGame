
module Chess where

import Data.Semigroup 
import Rule
import Nim
import Move
import Grp

type Vec1 = (Sum Int)
type Vec2 = (Sum Int, Sum Int)
type Vec3 = (Sum Int, Sum Int, Sum Int)

type ChessPiece = (Vec2, Vec2)
type ChessPieceMove = ChessPiece
type ChessPieceRule = Rule ChessPiece ChessPieceMove

type ChessGameState = [ChessPiece]
type ChessMove = (Select ChessPieceMove)
type ChessRule = Rule ChessGameState ChessMove


passBoard :: Rule Vec2 Vec2
passBoard = gate (\(x, y) -> x <  8
                          && x >= 0
                          && y <  8
                          && y >= 0)

passFriendly :: ChessRule
passFriendly = pass

passCapture :: ChessRule
passCapture = pass


inc :: Rule Vec1 Vec1
inc x = [Sum 1] 

rook :: ChessPieceRule
rook = ((pass /* pass) /*) $ (passBoard /.)
                      $         ((inv inc) /:/ 8 // inc /:/ 8) /* pass
                     // pass /* ((inv inc) /:/ 8 // inc /:/ 8)

bishop :: ChessPieceRule
bishop = ((pass /* pass) /*) $ (passBoard /.)
                        $ (    inc /*     inc) /:/ 8
                       // (    inc /* inv inc) /:/ 8
                       // (inv inc /*     inc) /:/ 8
                       // (inv inc /* inv inc) /:/ 8

queen = bishop // rook

knight :: ChessPieceRule
knight = ((pass /* pass) /*) $ (passBoard /.)
       $ (    inc /: 2 /* inv inc     )
      // (    inc      /* inv inc /: 2)
      // (    inc /: 2 /*     inc     )
      // (    inc      /*     inc /: 2)
      // (inv inc /: 2 /* inv inc     )
      // (inv inc      /* inv inc /: 2)
      // (inv inc /: 2 /*     inc     )
      // (inv inc      /*     inc /: 2)


capture :: ChessPieceRule
capture ((p, t), (x, y)) = [((mempty, mempty), (-x-1, -y-1))]


stringPiece :: ChessPiece -> String
stringPiece ((Sum p, Sum t), (Sum x, Sum y)) = case p of {0 -> "w"; 1 -> "b"; x -> "?"}
                                            ++ case t of {0 -> "K"; 1 -> "Q"; 2 -> "B";
                                                          3 -> "N"; 4 -> "R"; 5 -> "p"; x -> "?"}
                                            ++ case x of {0 -> "a"; 1 -> "b"; 2 -> "c"; 3 -> "d";
                                                          4 -> "e"; 5 -> "f"; 6 -> "g"; 7 -> "h"; x -> "?"}
                                            ++ show y
