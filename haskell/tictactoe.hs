module TicTacToe where
import Turn
import Rule
import Data.Bits

unoccupied :: (Bits b) => Int -> Char -> Rule [(Char, b)] (Char, b)
unoccupied total player = R {lambda = (\brd -> [(player, m) | m <- map (shift (bit 0)) [0..(total-1)], all ((== zeroBits) . (.&. m) . snd) brd]),
                      mu     = (\brd (mp, mi) -> [(p, o .|. mi) | (p, o) <- brd, p == mp] ++ [(p, o) | (p, o) <- brd, p /= mp]),
                      phi    = (\brd (mp, mi) -> [(p, (.|.) o $ complement mi) | (p, o) <- brd, p == mp] ++ [(p, o) | (p, o) <- brd, p /= mp])}

rowMask :: (Bits b, Num b) => Int -> Int -> Int -> [b]
rowMask rows columns win = [shift (fromInteger $ toInteger (2^win - 1)) (r * columns + c) | r <- [win..rows], c <- [win..columns]]

winByRow :: (Bits b, Num b) => Int -> Int -> Int -> Rule [(Char, b)] Char
winByRow rows columns win = R {lambda = (\brd -> [p | (p, o) <- brd, w <- rowMask rows columns win, (== zeroBits) $ (.&. w) $ complement o]), mu = const, phi = const}

tictactoe :: (Bits b) => Int -> Int -> Int -> Rule [(Char, b)] (Char, b)
tictactoe rows columns win = let {u = unoccupied (rows * columns) 'x'; r = winByRow rows columns win} in u

toPairs :: [a] -> [[a]]
toPairs [] = []
toPairs (x:[]) = [[x]]
toPairs (x:y:xs) = (++) [[x, y]] $ toPairs xs

pairdown string = [[x, y] | x <- ['a'..'z'], y <- ['a'..'z'], not $ elem [x, y] $ toPairs string]

validPairs [] = True
validPairs (x:[]) = False
validPairs (x:y:string) = (elem [x, y] $ pairdown string) && (validPairs string)


