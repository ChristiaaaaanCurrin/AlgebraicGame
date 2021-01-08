
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances     #-}
{-# LANGUAGE UndecidableInstances  #-}

module Nim where

import Move
import Grp
import Rule
import Data.Semigroup

instance (Num a) => Grp (Sum a) where
  inv = negate 

instance Num a => Move (Sum a) (Sum a) where
  (#) = (<>)

instance Enum a => Enum (Sum a) where
  toEnum = Sum . toEnum
  fromEnum (Sum x) = fromEnum x

nim :: Rule (Sum Int) (Sum Int)
nim (Sum n) = map Sum [-n.. -1]
