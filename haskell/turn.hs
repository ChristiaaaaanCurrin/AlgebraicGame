module Turn where
import Rule

simpleTurn :: [p] -> Rule (Int, p, s) s
simpleTurn players = R {lambda = (\(i, p, s) -> [s]),
                        mu     = (\(i, p, s) _ -> (i + 1, (cycle players)!!(i+1), s)),
                        phi    = (\(i, p, s) _ -> (i - 1, (cycle players)!!(i-1), s))}


