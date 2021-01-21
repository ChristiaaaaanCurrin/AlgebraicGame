
{-# LANGUAGE FlexibleContexts      #-}

module Chess where

import Data.Semigroup 
import Rule
import Move
import Group

data ChessPieceType = K | Q | B | N | R | P deriving (Read, Show, Eq)
instance Semigroup ChessPieceType where
  P <> x = x
  R <> R = N
  R <> N = B
  R <> B = Q
  R <> Q = K
  R <> K = P
  R <> x = x <> R
  N <> N = Q
  N <> B = K
  N <> Q = P
  N <> K = R
  N <> x = x <> N
  B <> B = P
  B <> Q = R
  B <> K = N
  B <> x = x <> B
  Q <> Q = N
  Q <> K = B
  Q <> x = x <> Q
  K <> K = Q
  K <> x = x <> K
instance Monoid ChessPieceType where
  mempty = P
instance Group ChessPieceType where
  inv P = P
  inv R = K
  inv N = Q
  inv B = B
  inv Q = N
  inv K = R
instance Move ChessPieceType ChessPieceType where
  x # y = x <> y
type ChessBoard   a = (a, a) -> Bool
type ChessPiece p a = ((p, ChessPieceType), (a, a))
type ChessState p a = (p, [ChessPiece p a])

type MovePattern a = SymRule (a, a)

sqU :: Num a => MovePattern (Sum a)
sqU = const $ pure (0, 1)
sqD :: Num a => MovePattern (Sum a)
sqD = inv sqU
sqR :: Num a => MovePattern (Sum a)
sqR = const $ pure (1, 0)
sqL :: Num a => MovePattern (Sum a)
sqL = inv sqR

diagI :: Num a => MovePattern (Sum a)
diagI = sqU /. sqR
diagII :: Num a => MovePattern (Sum a)
diagII = sqU /. sqL
diagIII :: Num a => MovePattern (Sum a)
diagIII = inv diagI 
diagIV :: Num a => MovePattern (Sum a)
diagIV = inv diagII 

passBoard :: (Ord a, Num a, Group m) => Rule (ChessPiece p a, [ChessPiece p a]) m
passBoard = gate $ (\((t, (x, y)), xs) -> 0 < x && x <= 8 && 0 < y && y <= 8)
passFriendly :: (Eq a, Eq p, Group m) => Rule (ChessPiece p a, [ChessPiece p a]) m
passFriendly = gate $ (\(((p, t), x), xs) -> null [x |((p', t'), x') <- xs, p' == p, x' == x])
passCapture :: Monoid m => Rule (ChessPiece p a, [ChessPiece p a]) m
passCapture = pass
passNoCapture :: Monoid m => Rule (ChessPiece p a, [ChessPiece p a]) m
passNoCapture = pass
passCheck :: Monoid m => Rule (ChessState p a) m
passCheck = pass

kleeneStar r = (passBoard /. passFriendly /. passNoCapture /. ((pass /* r) /* pass) /. passBoard) //: 8

type IntPiece = ChessPiece (Sum Int) (Sum Int)
type IntPieceMove = ((Sum Int, ChessPieceType),  (Sum Int, Sum Int))

rookMove :: Rule (IntPiece, [IntPiece]) (IntPieceMove, Select IntPieceMove)
rookMove = kleeneStar sqU // kleeneStar sqD // kleeneStar sqR // kleeneStar sqL

