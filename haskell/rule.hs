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

data Inv b = I b
instance (Rule a b) => Rule a (Inv b) where
  lambda = map I . lambda
  phi (I y) = rho y
  rho (I y) = phi y

instance (Eq a, Rule a b) => Rule [a] (a, b) where
  lambda xs = [(x, y) | x <- xs, y <- lambda x]
  phi (x, y) = (:) (phi y x) . filter (/=x)
  rho (x, y) = (:) (rho y x) . filter (/=x)

infixl 9 `X`
data X b d =  X b d deriving (Eq, Read, Show)
instance (Rule a b, Rule c d) => Rule (a, c) (X b d) where
  lambda (a, c)        = [X b d | b <- lambda a, d <- lambda c]
  phi    (X b d) (a, c) = (phi b a, phi d c)
  rho    (X b d) (a, c) = (rho b a, rho d c)

infixl 8 `Y`
data Y b c = Y b c deriving (Eq, Read, Show)
instance (Rule a b, Rule a c) => Rule a (Y b c) where
  lambda x         = [Y y z | y <- lambda x, z <- lambda x]
  phi   (Y y z) = phi y . phi z
  rho   (Y y z) = rho z . rho y

infixr 7 `Z`
data Z b c = Z b c deriving (Eq, Read, Show)
instance (Rule a b, Rule (a, b) c) => Rule a (Z b c) where
  lambda x = [Z y z | y <- lambda x, z <- lambda (x, y)] 
  phi   (Z y z) = fst . phi z . (,y) . phi y
  rho   (Z y z) = (uncurry $ flip $ rho) . rho z . (,y)

data R a = R a deriving (Eq, Read, Show)

infixl 6 `G`
data G c = G c deriving (Eq, Read, Show)
instance (Eq a, Rule (R a) (R a), Rule a c) => Rule a (G c) where
  lambda x
    | R x `elem` lambda (R x) = map G $ lambda x
    | otherwise = []
  phi (G y) = phi y
  rho (G y) = rho y

instance (Rule a b, Rule c d) => Rule (a, c) (Either b d) where
  lambda (x, y) = (map Left  $ lambda x) ++ (map Right $ lambda y)
  phi ez (x, y) = case ez of {Left  z -> (phi z x, y); Right z -> (x, phi z y)}
  rho ez (x, y) = case ez of {Left  z -> (rho z x, y); Right z -> (x, rho z y)}

newtype Turn = T Int deriving (Eq, Show, Read, Ord)
instance Rule Int Turn where
  lambda  = map T . pure
  phi (T y) x = y + 1
  rho (T y) x = y - 1

instance Num Turn where
  (+) (T x) (T y) = T $ x + y
  (*) (T x) (T y) = T $ x * y
  abs       (T x) = T $ abs x
  signum    (T x) = T $ signum x
  negate    (T x) = T $ negate x
  fromInteger     = T . fromInteger

newtype Nim a = N a deriving (Eq, Show, Read, Ord)
instance (Num a, Enum a) => Rule a (Nim a) where
  lambda n = map N [1..n]
  phi (N m) n = n - m 
  rho (N m) n = n + m

instance Num a => Num (Nim a) where
  (+) (N x) (N y) = N (x + y)
  (*) (N x) (N y) = N (x * y)
  abs       (N x) = N $ abs x
  signum    (N x) = N $ signum x
  negate    (N x) = N $ negate x
  fromInteger i   = N $ fromInteger i

instance Enum a => Enum (Nim a) where
  toEnum i = N $ toEnum i
  fromEnum (N i) = fromEnum i

instance Real a => Real (Nim a) where
  toRational (N i) = toRational i

instance Integral a => Integral (Nim a) where
  toInteger (N i) = toInteger i
  quotRem (N i) (N j) = (N $ fst $ quotRem i j, N $ fst $ quotRem i j) 

