{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE MultiParamTypeClasses #-}

module Nim where

import Rule

--Nim Sum
instance Rule a b => Rule [a] (Int, b) where
  lambda xs = [(i, y) | (i, x) <- zip [0..] xs, y <- lambda x]
  phi (i, y) xs = (++) (take i xs) $ (:) (phi y (xs!!i)) $ drop (i+1) xs
  rho (i, y) xs = (++) (take i xs) $ (:) (rho y (xs!!i)) $ drop (i+1) xs

newtype Nim a = N a deriving (Eq, Show, Read, Ord)
instance (Num a, Enum a) => Rule a (Nim a) where
  lambda n = map N [1..n]
  phi (N m) n = n - m 
  rho (N m) n = n + m

--Constant Form
instance (Enum a) => Rule a a where
  lambda = pure
  phi    = const . succ
  rho    = const . pred

