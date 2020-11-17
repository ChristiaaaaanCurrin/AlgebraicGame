
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances     #-}
{-# LANGUAGE UndecidableInstances  #-}
{-# LANGUAGE AllowAmbiguousTypes   #-}

module Inv  where

import Move

infixr 8 %

class Inv m where
  (%)  :: m -> m -> m
  inv  :: m -> m
  pass :: m

instance Num a => Inv a where
  (%) = (+)
  inv = negate
  pass = 0

instance (Inv b, Inv d) => Inv (b, d) where 
  (%)  (y1, w1) (y2, w2) = (y1 % y2, w1 % w2)
  inv  (y, w) = (inv y, inv w)
  pass = (pass, pass)

instance (Inv b, Inv c) => Inv (Either b c) where
  (%)  (Left  y1) (Left  y2) = Left  $ y1 % y2
  (%)  (Right y1) (Right y2) = Right $ y1 % y2
  inv  (Left  y) = Left  $ inv  y
  inv  (Right y) = Right $ inv  y
  pass = Left  pass

instance (Inv b) => Inv [b] where
  (%) = (++)
  inv  ys = map inv $ reverse ys
  pass = pure pass

instance (Inv b) => Inv (Select b) where
  (%) (Select is y1) (Select js y2) = Select is (y1 % y2)
  inv (Select is y) = Select is (inv y)
  pass = Select [0] pass
