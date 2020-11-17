
module Nim where

import Move
import Inv
import Rule

nim :: Rule Int Int
nim n = [-n.. -1]


