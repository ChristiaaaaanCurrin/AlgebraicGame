 
{-# LANGUAGE MultiParamTypeClasses #-}

import Data.Semigroup
import Move
import Group
import Rule

module Sum where

instance (Num a) => Group (Sum a) where
  inv = negate

instance (Num a) => Move (Sum a) (Sum a) where
  (#) = (<>)


