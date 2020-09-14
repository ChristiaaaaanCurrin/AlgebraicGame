data Rule a b = R {lambda :: a -> [b], mu :: a -> b -> a, phi :: a ->  b -> a}

union :: Rule a b -> Rule a b -> Rule a b
union r s = R {lambda = (\x -> (lambda r x) ++ (lambda s x)),
               mu     = mu  r,
               phi    = phi r}

intersection :: Eq b => Rule a b -> Rule a b -> Rule a b
intersection r s = R {lambda = (\x -> [y | y <- lambda r x, y `elem` lambda s x]),
                      mu     = mu  r,
                      phi    = phi r}

independentProduct :: Rule a b -> Rule a c -> Rule a (b, c)
independentProduct r s = R {lambda = (\x -> [(yr, ys) | yr <- lambda r x, ys <- lambda s x]),
                            mu     = (\x (y, z) -> mu  r (mu  s x z) y),
                            phi    = (\x (y, z) -> phi s (phi r x y) z)}

dependentProduct :: Rule b c -> Rule a b -> Rule a (b, c)
dependentProduct s r = R {lambda = (\x -> [(y, z) | y <- lambda r x, z <- lambda s y]),
                          mu     = (\x (y, z) -> mu  r x $ mu  s y z),
                          phi    = (\x (y, z) -> phi r x $ phi s y z)}

contradict :: Rule a a -> Rule a a
contradict r = R {lambda = (\x -> case () of 
                                           _ | null $ lambda r x -> [x]
                                             | otherwise -> []),
                  mu = mu r,
                  phi = phi r}
               
(/|) r s = union r s
(/&) r s = intersection r s
(/-) = contradict
(/.) = dependentProduct
(/*) = independentProduct

patternStep :: (a -> [a]) -> (a -> Bool) -> a -> [a]
patternStep step stop x
  | stop x = [x]
  | otherwise = (++) [x] $ mconcat . map (patternStep step stop) $ step x

pattern :: Rule b b -> Rule a b -> Rule b c -> Rule a b
pattern r s t = R {lambda = concat . map (patternStep (lambda r) (null . lambda t)) . lambda s,
                   mu     = (\x y -> mu s x $ mu r y y),
                   phi    = (\x y -> phi s x $ phi r y y)}

passRule :: Rule a a
passRule = R {lambda = pure . id, mu = const, phi = const}

constRule :: b -> Rule a b
constRule y = R {lambda = pure . const y, mu = const, phi = const}

falseRule :: Rule a a
falseRule = R {lambda = const [], mu = const, phi = const}


data TTCS = TTCS {toMove :: Char, players :: [(Char, Int)]}

