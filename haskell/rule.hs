{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleContexts      #-}

module Rule where

import Move
import Inv

type Rule a b = a -> [b]
instance Inv b => Inv (Rule a b) where
  (r % s) x = [z % y | z <- r x, y <- s x]
  (inv r) x = map inv $ r x
  pass x = [pass]

gate :: Inv b => (a -> Bool) -> Rule a b
gate f x
  | f x = [pass]
  | otherwise = []

(/*) :: Rule a b -> Rule c d -> Rule (a, c) (b, d)
(r /* s) (x, z) = [(y, w) | y <- r x, w <- s z]

(/./) :: Rule a b -> Rule a c -> Rule a [Either b c]
(r /./ s) x = [[Left y, Right z] | y <- r x, z <- s x]

(//) :: Rule a b -> Rule a b -> Rule a b
(r // s) x = (r x) ++ (s x)

(/-/) :: Rule a b -> Rule a c -> Rule a (Either b c)
(r /-/ s) x = (map Left $ r x) ++ (map Right $ s x)

(/\) :: (Eq b) => Rule a b -> Rule a b -> Rule a b
(r /\ s) x = [y | y <- s x, y `elem` r x]

r /+ s = (r /* pass) /-/ (pass /* s) 

