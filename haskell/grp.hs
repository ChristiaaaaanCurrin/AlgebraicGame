
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances     #-}
{-# LANGUAGE UndecidableInstances  #-}
{-# LANGUAGE AllowAmbiguousTypes   #-}

module Grp  where

import Move

class Monoid m => Grp m where
  inv  :: m -> m

instance (Grp b, Grp d) => Grp (b, d) where 
  inv  (y, w) = (inv y, inv w)

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



