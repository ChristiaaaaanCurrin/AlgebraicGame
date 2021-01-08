
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances     #-}
{-# LANGUAGE FlexibleContexts      #-}

module Rule where

import Move
import Grp

graph :: Move a b => Rule a b -> a -> [a]
graph r x = map (# x) $ r x

type Rule a b = a -> [b]
instance Grp b => Grp (Rule a b) where
  inv r x = map inv $ r x

rule0 :: Rule a b
rule0 x = []

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

infixr 8 /.
(r /. s) x = [z <> y | y <- s x, z <- r (y # x)]

infixl 9 /:
(/:) :: (Move a b, Grp b) => Rule a b -> Int -> Rule a b
r /: n 
  | n <= 1 = r
  | otherwise = r /. r /: (n - 1)

infixr 8 /./
(/./) :: Move a b => Rule a c -> Rule a b -> Rule a [Either c b]
(r /./ s) x = [[Left z, Right y] | y <- s x, z <- r (y # x)]

infixr 7 /*
(/*) :: Rule a b -> Rule c d -> Rule (a, c) (b, d)
(r /* s) (x, z) = [(y, w) | y <- r x, w <- s z]

infixl 6 /\
(/\) :: (Eq b) => Rule a b -> Rule a b -> Rule a b
(r /\ s) x = [y | y <- s x, y `elem` r x]

infixl 5 //
(//) :: Rule a b -> Rule a b -> Rule a b
(r // s) x = (r x) ++ (s x)

infixr 5 /-/
(/-/) :: Rule a b -> Rule a c -> Rule a (Either b c)
(r /-/ s) x = (map Left $ r x) ++ (map Right $ s x)

infixl 4 /+
r /+ s = (r /* pass) /-/ (pass /* s) 

infixl 9 /:/
r /:/ n
  | n <= 1 = r
  | otherwise = r /: n // r /:/ (n - 1)
