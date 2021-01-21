

module FiniteGroup where

import Group

mod' :: (Ord a, Num a) => a -> a -> a
mod' x m
  | x == 0 || x == m = 0
  | m <  0 = (+ m) $ mod' x (-m)
  | x >  m = mod' (x - m) m
  | x <  0 = mod' (x + m) m
  | otherwise = x

data Cyclic a = Cyclic a a deriving (Read, Show)
instance (Eq a, Num a, Ord a) => Eq (Cyclic a) where
  Cyclic m x == Cyclic n y = mod' x m == mod' y n
instance (Ord a, Num a) => Semigroup (Cyclic a) where
  Cyclic m x <> Cyclic n y = Cyclic (x + y) (max m n)
instance (Ord a, Num a) => Monoid (Cyclic a) where
  mempty = Cyclic 0 0
instance (Ord a, Num a) => Group (Cyclic a) where
  inv (Cyclic m x) = Cyclic m (-x)
