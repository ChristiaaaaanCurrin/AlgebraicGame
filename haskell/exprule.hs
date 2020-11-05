{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE FlexibleInstances #-}
module Rule where

class Rule r a b where
  phi :: r -> b -> a -> a
  rho :: r -> b -> a -> a
  lambda :: r -> a -> [b]
 
data RuleBuilder a b = R (a -> [b]) (b -> a -> a) (b -> a -> a)
instance Rule (RuleBuilder a b) a b where
  lambda (R l p r) = l
  phi (R l p r) = p
  rho (R l p r) = r 

data Union r s = U r s
instance (Rule r a b, Rule s a b) => Rule (Union r s) a b where
  lambda (U r s) x = (++) (lambda r x) (lambda s x)
  phi (U r s) = phi r
  rho (U r s) = rho r

data Intersection r s = N r s
instance (Rule r a b, Rule s a b, Eq b) => Rule (Intersection r s) a b where
  lambda (N r s) x = [y | y <- lambda r x, y `elem` lambda s x] 
  phi (N r s) = phi r
  rho (N r s) = rho r

