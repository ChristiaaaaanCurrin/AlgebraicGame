{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TupleSections #-} 
{-# LANGUAGE TypeOperators #-}
{-# LANGUAGE UndecidableInstances #-}
{-# LANGUAGE AllowAmbiguousTypes #-}
{-# LANGUAGE FlexibleContexts #-}

module Rule where

class Rule a b where
  lambda :: a -> [b]
  phi    :: b -> a -> a
  rho    :: b -> a -> a

--Inverse
data Inv b = I b
instance (Rule a b) => Rule a (Inv b) where
  lambda = map I . lambda
  phi (I y) = rho y
  rho (I y) = phi y

--Lift
instance (Eq a, Rule a b) => Rule [a] (a, b) where
  lambda xs = [(x, y) | x <- xs, y <- lambda x]
  phi (x, y) = (:) (phi y x) . filter (/=x)
  rho (x, y) = (:) (rho y x) . filter (/=x)

--Reduction / Gate
infixl 6 `G`
data G c = G c deriving (Eq, Read, Show)
data R a = R a deriving (Eq, Read, Show)
instance (Eq a, Rule (R a) (R a), Rule a c) => Rule a (G c) where
  lambda x
    | R x `elem` lambda (R x) = map G $ lambda x
    | otherwise = []
  phi (G y) = phi y
  rho (G y) = rho y

--Game Sum
instance (Rule a b, Rule c d) => Rule (a, c) (Either b d) where
  lambda (x, y) = (map Left  $ lambda x) ++ (map Right $ lambda y)
  phi ez (x, y) = case ez of {Left  z -> (phi z x, y); Right z -> (x, phi z y)}
  rho ez (x, y) = case ez of {Left  z -> (rho z x, y); Right z -> (x, rho z y)}

--Full Product
infixl 9 `X`
data X b d =  X b d deriving (Eq, Read, Show)
instance (Rule a b, Rule c d) => Rule (a, c) (X b d) where
  lambda (a, c)        = [X b d | b <- lambda a, d <- lambda c]
  phi    (X b d) (a, c) = (phi b a, phi d c)
  rho    (X b d) (a, c) = (rho b a, rho d c)

--Fork Product
infixl 8 `Y`
data Y b c = Y b c deriving (Eq, Read, Show)
instance (Rule a b, Rule a c) => Rule a (Y b c) where
  lambda x         = [Y y z | y <- lambda x, z <- lambda x]
  phi   (Y y z) = phi y . phi z
  rho   (Y y z) = rho z . rho y

--Dependent Product
infixr 7 `Z`
data Z b c = Z b c deriving (Eq, Read, Show)
instance (Rule a b, Rule (a, b) c) => Rule a (Z b c) where
  lambda x = [Z y z | y <- lambda x, z <- lambda (x, y)] 
  phi   (Z y z) = fst . phi z . (,y) . phi y
  rho   (Z y z) = (uncurry $ flip $ rho) . rho z . (,y)

