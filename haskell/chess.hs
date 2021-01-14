
module Chess where

import Data.Semigroup 
import Rule
import Move
import Grp

data ChessPiece p i a = K p i a a
                      | Q p i a a
                      | B p i a a
                      | N p i a a
                      | R p i a a
                      | P p i a a

data ChessBoard a = ChessBoard a a

type ChessState p i a = (p, ChessBoard a, [ChessPiece p i a])

