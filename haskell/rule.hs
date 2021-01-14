
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances     #-}
{-# LANGUAGE FlexibleContexts      #-}

module Rule (
  Rule, SymRule,
  graph,
  void, pass, gate, lift, funLift,
  (/.), (/./), (/:), (//:),
  (/*),
  (//), (/\), (/-/),
  (/+)
  ) where

import Move
import Grp

type Rule a b = a -> [b]
instance Grp b => Grp (Rule a b) where
  inv r x = map inv $ r x

type SymRule a = Rule a a

graph :: Move a b => Rule a b -> a -> [a]
graph r x = map (# x) $ r x

void :: Rule a b
void x = []

pass :: Monoid b => Rule a b
pass x = [mempty]

gate :: Grp b => (a -> Bool) -> Rule a b
gate f x
  | f x = [mempty]
  | otherwise = []

liftStep :: Int -> Rule a b -> Rule [a] (Select b)
liftStep i r [] = []
liftStep i r (x:xs) = map (Select [i]) (r x) ++ (liftStep (i + 1) r xs)

lift = liftStep 0

funLift :: [a] -> (a -> Rule b m) -> Rule (a -> b) (a -> m)
funLift xs t s = [\y -> z | x <- xs, z <- t x $ s x]

infixr 8 /. -- Dot Product (Closed)
(r /. s) x = [z <> y | y <- s x, z <- r (y # x)]

infixl 9 /: -- Power
(/:) :: (Move a b, Grp b) => Rule a b -> Int -> Rule a b
r /: n 
  | n <= 1 = r
  | otherwise = r /. r /: (n - 1)

infixl 9 //: --  Union Power
r //: n
  | n <= 1 = r
  | otherwise = r /: n // r //: (n - 1)

infixr 8 /./ -- Dot Product (Robust Version)
(/./) :: Move a b => Rule a c -> Rule a b -> Rule a [Either c b]
(r /./ s) x = [[Left z, Right y] | y <- s x, z <- r (y # x)]

infixr 7 /* -- Cross Product
(/*) :: Rule a b -> Rule c d -> Rule (a, c) (b, d)
(r /* s) (x, z) = [(y, w) | y <- r x, w <- s z]

infixl 6 /\  -- Intersection
(/\) :: (Eq b) => Rule a b -> Rule a b -> Rule a b
(r /\ s) x = [y | y <- s x, y `elem` r x]

infixl 5 // -- Union
(//) :: Rule a b -> Rule a b -> Rule a b
(r // s) x = (r x) ++ (s x)

infixr 5 /-/ -- Disjoint Union
(/-/) :: Rule a b -> Rule a c -> Rule a (Either b c)
(r /-/ s) x = (map Left $ r x) ++ (map Right $ s x)

infixl 4 /+ -- Sum
r /+ s = (r /* pass) /-/ (pass /* s) 

