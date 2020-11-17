
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances     #-}
{-# LANGUAGE UndecidableInstances  #-}
{-# LANGUAGE AllowAmbiguousTypes   #-}

module Move where

infixr #
class Move a m where
  (#) :: m -> a -> a

instance Num a => Move a a where
  (#) = (+)

instance (Move a b, Move c d) => Move (a, c) (b, d) where
  (#) (y, w) (x, z) = (y # x, w # z)

instance (Move a b) => Move a [b] where
  (#) [] x = x
  (#) (y:ys) x = ys # y # x

instance (Move a b, Move a c) => Move a (Either b c) where
  (Left  y) # x = y # x
  (Right y) # x = y # x

data Select b = Select [Int] b deriving (Show, Read, Eq, Ord)
instance (Move a b) => Move [a] (Select b) where
  (#) (Select []     y) xs = xs 
  (#) (Select (i:is) y) xs = (Select is y) # ((++) (take i xs) $ (y # (xs!!i)):(drop (i+1) xs))
