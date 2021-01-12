
module Chess where

import Data.Semigroup 
import Rule
import Vec
import Move
import Grp

type ChessPiece = ((Sum Int, Sum Int), (Sum Int, Sum Int))
type ChessPieceMove = ChessPiece
type ChessPieceRule = Rule ChessPiece ChessPieceMove

type ChessGameState = [ChessPiece]
type ChessMove = (Select ChessPieceMove)
type ChessRule = Rule ChessGameState ChessMove

board = ((0, 8), (0, 8))

friendlyFire (((p, _), (x, y)):pcs) = any id [x' == x && y' == y && p' == p | ((p', k), (x', y')) <- pcs] || friendlyFire pcs
passFriendly :: ChessRule
passFriendly = gate friendlyFire

detectCapture (((p, _), (x, y)):pcs) = any id [x' == x && y' == y && p' /= p | ((p', k), (x', y')) <- pcs] || detectCapture pcs
passCapture :: ChessRule
passCapture = gate detectCapture

rook :: ChessPieceRule
rook = void 

bishop :: ChessPieceRule
bishop = ((pass /* pass) /*) $ (passBoard2 board /.)
                        $ (vec2   1    1 ) /:/ 8
                       // (vec2   1  (-1)) /:/ 8
                       // (vec2 (-1)   1 ) /:/ 8
                       // (vec2 (-1) (-1)) /:/ 8

queen = bishop // rook

knight :: ChessPieceRule
knight = ((pass /* pass) /*)
       $ (passBoard2 board /.)
       $ foldr (//) void [vec2 (f i) (g j) | (i, j) <- [(1, 2), (2, 1)], f <- [negate, id], g <- [negate, id]]

capture :: ChessPieceRule
capture = pass /* (inc /: 8 /* inc /: 8)


stringPiece :: ChessPiece -> String
stringPiece ((Sum p, Sum t), (Sum x, Sum y)) = case p of {0 -> "w"; 1 -> "b"; x -> "?"}
                                            ++ case t of {0 -> "K"; 1 -> "Q"; 2 -> "B";
                                                          3 -> "N"; 4 -> "R"; 5 -> "p"; x -> "?"}
                                            ++ case x of {0 -> "a"; 1 -> "b"; 2 -> "c"; 3 -> "d";
                                                          4 -> "e"; 5 -> "f"; 6 -> "g"; 7 -> "h"; x -> "?"}
                                            ++ show y
