module Rule where

data Rule a b = R {lambda :: a -> [b], phi :: a -> b -> a, rho :: a ->  b -> a}


complement :: Rule a b -> Rule a a
complement r = R {lambda = (\x -> case (lambda r x) of {[] -> [x]; xs -> [x]}),
                  phi    = const,
                  rho    = const}

reduction :: Rule a b -> Rule a a
reduction r = R {lambda = (\x -> case (lambda r x) of {[] -> []; xs -> [x]}),
                 phi    = const,
                 rho    = const}

union :: Rule a b -> Rule a b -> Rule a b
union r s = R {lambda = (\x -> (lambda r x) ++ (lambda s x)),
               phi    = phi r,
               rho    = rho r}

disjointUnion :: Rule a b -> Rule a c -> Rule a (Either b c)
disjointUnion r s = R {lambda = (\x -> (map Left $ lambda r x) ++ (map Right $ lambda s x)),
                       phi    = (\x y -> case y of {Left z -> phi r x z; Right z -> phi s x z}),
                       rho    = (\x y -> case y of {Left z -> rho r x z; Right z -> rho s x z})}

intersection :: Eq b => Rule a b -> Rule a b -> Rule a b
intersection r s = R {lambda = (\x -> [y | y <- lambda r x, y `elem` lambda s x]),
                      phi    = phi r,
                      rho    = rho r}

independentProduct :: Rule a c -> Rule a b -> Rule a (b, c)
independentProduct s r = R {lambda = (\x -> [(yr, ys) | yr <- lambda r x, ys <- lambda s x]),
                            phi    = (\x (y, z) -> phi r (phi s x z) y),
                            rho    = (\x (y, z) -> rho s (rho r x y) z)}

dependentProduct :: Rule b c -> Rule a b -> Rule a (b, c)
dependentProduct s r = R {lambda = (\x -> [(y, z) | y <- lambda r x, z <- lambda s y]),
                          phi    = (\x (y, z) -> phi r x $ phi s y z),
                          rho    = (\x (y, z) -> rho r x $ phi s y z)}

                          --rho    = (\(y, z) -> rho r $ phi s z y )}
                          --rho    = rho r . (uncurry $ phi s)

fullProduct :: Rule c d -> Rule a b -> Rule (a, c) (b, d)
fullProduct s r = R {lambda = (\(a, c) -> [(b, d) | b <- lambda r a, d <- lambda s c]),
                     phi    = (\(a, c) (b, d) -> (phi r a b, phi s c d)),
                     rho    = (\(a, c) (b, d) -> (rho r a b, rho s c d))}

patternStep :: (a -> [a]) -> (a -> Bool) -> a -> [a]
patternStep step stop x
  | stop x = [x]
  | otherwise = (++) [x] $ mconcat . map (patternStep step stop) $ step x

pattern :: Rule b b -> Rule a b -> Rule b c -> Rule a b
pattern r s t = R {lambda = concat . map (patternStep (lambda r) (null . lambda t)) . lambda s,
                   phi    = (\x y -> phi s x $ phi r y y),
                   rho    = (\x y -> rho s x $ rho r y y)}

voidRule :: Rule a b
voidRule = R {lambda = const [], phi = const, rho = const}

passRule :: Rule a a
passRule = R {lambda = pure, phi = const, rho = const}

(/-) = complement
(/+) = reduction
(/\) r s = intersection r s
(//) = union
(/-/) = disjointUnion
(/.) = dependentProduct
(/*) = independentProduct
(/**) = fullProduct

