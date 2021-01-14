
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances     #-}
{-# LANGUAGE UndecidableInstances  #-}
{-# LANGUAGE AllowAmbiguousTypes   #-}

module Grp  where

import Move
import Data.Semigroup


class Monoid m => Grp m where
  inv  :: m -> m

instance Monoid m => Move m m where
  (#) = (<>)


instance (Grp b1, Grp b2) => Grp (b1, b2) where 
  inv  (y1, y2) = (inv y1, inv y2)

instance (Grp b1, Grp b2, Grp b3) => Grp (b1, b2, b3) where 
  inv  (y1, y2, y3) = (inv y1, inv y2, inv y3)

instance (Grp b1, Grp b2, Grp b3, Grp  b4) => Grp (b1, b2, b3, b4) where 
  inv  (y1, y2, y3, y4) = (inv y1, inv y2, inv y3, inv y4)

instance (Grp b1, Grp b2, Grp b3, Grp b4, Grp b5) => Grp (b1, b2, b3, b4, b5) where 
  inv  (y1, y2, y3, y4, y5) = (inv y1, inv y2, inv y3, inv y4, inv y5)


instance (Monoid b, Monoid c) => Monoid (Either b c) where
  mempty = Left  mempty


instance (Grp b, Grp c) => Grp (Either b c) where
  inv  (Left  y) = Left  $ inv  y
  inv  (Right y) = Right $ inv  y


instance (Grp b) => Grp [b] where
  inv  ys = map inv $ reverse ys


instance (Semigroup b) => Semigroup (Select b) where
  (<>) (Select is y1) (Select js y2) = Select is (y1 <> y2)

instance (Monoid b) => Monoid (Select b) where
  mempty = Select [0] mempty

instance (Grp b) => Grp (Select b) where
  inv (Select is y) = Select is (inv y)


instance (Num a) => Grp (Sum a) where
  inv = negate


