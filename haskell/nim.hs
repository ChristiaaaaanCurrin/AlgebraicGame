
module Nim where

import Rule
import Data.Semigroup

instance Enum a => Enum (Sum a) where
  toEnum x = Sum (toEnum x)
  fromEnum (Sum x) = fromEnum x

nim :: Rule (Sum Int) (Sum Int)
nim n = [-n.. -1]
