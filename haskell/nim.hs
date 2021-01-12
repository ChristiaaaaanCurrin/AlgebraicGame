
module Nim where

import Vec
import Rule

nim :: Rule Vec1 Vec1
nim n = [-n.. -1]
