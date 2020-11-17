{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleContexts      #-}

module Rule where

import Move
import Inv


class InvR r where
  (/%)  :: r -> r -> r
  invR  :: r -> r
  passR :: r

graph :: Move a b => Rule a b -> a -> [a]
graph r x = map (# x) $ r x

type Rule a b = a -> [b]
instance Inv b => InvR (Rule a b) where
  (r /% s) x = [z % y | z <- r x, y <- s x]
  invR r x = map inv $ r x
  passR x = [pass]

gate :: Inv b => (a -> Bool) -> Rule a b
gate f x
  | f x = pure pass
  | otherwise = []

liftStep :: Int -> Rule a b -> Rule [a] (Select b)
liftStep i r [] = []
liftStep i r (x:xs) = map (Select [i]) (r x) ++ (liftStep (i + 1) r xs)

lift = liftStep 0

infixl 9 /:
(/:) :: Inv b => Rule a b -> Int -> Rule a b
r /: 1 = r
r /: n = r /% r /: (n - 1)

infixr 8 /.
(/.) :: Rule a b -> Rule a c -> Rule a [Either b c]
(r /. s) x = [[Left y, Right z] | y <- r x, z <- s x]

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

