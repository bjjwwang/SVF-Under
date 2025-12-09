from Assignment_3_Helper import *
import z3
import pysvf

class Assignment3(AbstractExecution):
    def __init__(self, pag: pysvf.SVFIR) -> None:
        super().__init__(pag)

    #TODO : Implement the state updates for Copy, Binary, Store, Load, Gep, Phi
    # TODO: your code starts from here
    def updateStateOnGep(self, gep: pysvf.GepStmt):
        node = gep.getICFGNode()
        abstract_state = self.post_abs_trace[node]
        assert isinstance(abstract_state, AbstractState)
        lhs = gep.getLHSVarID()
        rhs = gep.getRHSVarID()
        if abstract_state.getVar(rhs).isAddr():
            offset = abstract_state.getElementIndex(gep)
            abstract_state[lhs] = abstract_state.getGepObjAddrs(rhs, offset)

    #TODO: your code starts from here
    def updateStateOnStore(self, store: pysvf.StoreStmt):
        node = store.getICFGNode()
        abstract_state = self.post_abs_trace[node]
        assert isinstance(abstract_state, AbstractState)
        lhs = store.getLHSVarID()
        rhs = store.getRHSVarID()
        if abstract_state.getVar(lhs).isAddr():
            abstract_state.storeValue(lhs, abstract_state[rhs])

    #TODO: your code starts from here
    # Find the comparison predicates in "class BinaryOPStmt:OpCode" under SVF/svf/include/SVFIR/SVFStatements.h
    # You are required to handle predicates (The program is assumed to have signed ints and also interger-overflow-free),
    # including Add, FAdd, Sub, FSub, Mul, FMul, SDiv, FDiv, UDiv, SRem, FRem, URem, Xor, And, Or, AShr, Shl, LShr
    def updateStateOnBinary(self, binary: pysvf.BinaryOPStmt):
        node = binary.getICFGNode()
        abstract_state = self.post_abs_trace[node]
        lhs = binary.getResId()
        op1 = binary.getOpVar(0)
        op2 = binary.getOpVar(1)
        assert abstract_state.getVar(op1.getId()).isInterval() and abstract_state.getVar(op2.getId()).isInterval()
        result = IntervalValue(0)
        val1 = abstract_state[op1.getId()].getInterval()
        val2 = abstract_state[op2.getId()].getInterval()
        assert(isinstance(val1, IntervalValue) and isinstance(val2, IntervalValue))
        if binary.getOpcode() == OpCode.Add or binary.getOpcode() == OpCode.FAdd:
            result = val1 + val2
        elif binary.getOpcode() == OpCode.Sub or binary.getOpcode() == OpCode.FSub:
            result = val1 - val2
        elif binary.getOpcode() == OpCode.Mul or binary.getOpcode() == OpCode.FMul:
            result = val1 * val2
        elif binary.getOpcode() == OpCode.UDiv or binary.getOpcode() == OpCode.SDiv or binary.getOpcode() == OpCode.FDiv:
            if int(val2.ub())>=0 and int(val2.lb()) <= 0:
                result = IntervalValue.top()
            else:
                result = val1 / val2
        elif binary.getOpcode() == OpCode.SRem or binary.getOpcode() == OpCode.FRem or binary.getOpcode() == OpCode.URem:
            if int(val2.ub())>=0 and int(val2.lb()) <= 0:
                result = IntervalValue.top()
            else:
                result = val1 % val2
        elif binary.getOpcode() == OpCode.Xor:
            result = val1 ^ val2
        elif binary.getOpcode() == OpCode.Or:
            result = val1 | val2
        elif binary.getOpcode() == OpCode.And:
            result = val1 & val2
        elif binary.getOpcode() == OpCode.Shl:
            result = val1 << val2
        elif binary.getOpcode() == OpCode.LShr or binary.getOpcode() == OpCode.AShr:
            result = val1 >> val2
        else:
            result = IntervalValue.top()
        abstract_state[lhs] = AbstractValue(result)


    #TODO: your code starts from here
    def updateStateOnLoad(self, load: pysvf.LoadStmt):
        node = load.getICFGNode()
        abstract_state = self.post_abs_trace[node]
        assert isinstance(abstract_state, AbstractState)
        lhs = load.getLHSVarID()
        rhs = load.getRHSVarID()
        if abstract_state.getVar(rhs).isAddr():
            abstract_state[lhs] = abstract_state.loadValue(rhs)
        else:
            abstract_state[lhs] = AbstractValue(IntervalValue.top())

    #TODO: your code starts from here
    def updateStateOnCopy(self, copy: pysvf.CopyStmt):
        node = copy.getICFGNode()
        abstract_state = self.post_abs_trace[node]
        abstract_state[copy.getLHSVarID()] = abstract_state[copy.getRHSVarID()]

    # TODO: your code starts from here
    def updateStateOnPhi(self, phi: pysvf.PhiStmt):
        node = phi.getICFGNode()
        abstract_state = self.post_abs_trace[node]
        lhs = phi.getResId()
        result = AbstractValue()
        for i in range(phi.getOpVarNum()):
            op_var = phi.getOpVar(i)
            if abstract_state.getVar(op_var.getId()).isInterval() or abstract_state.getVar(op_var.getId()).isAddr():
                result.join_with(abstract_state[op_var.getId()])
        abstract_state[lhs] = result

    """
    Handle ICFG nodes in a cycle using widening and narrowing operators.
    
    This function implements abstract interpretation for cycles in the ICFG using widening and narrowing
    operators to ensure termination. It processes all ICFG nodes within a cycle and implements
    widening-narrowing iteration to reach fixed points twice: once for widening (to ensure termination)
    and once for narrowing (to improve precision).
    
    :param cycle: The WTO cycle containing ICFG nodes to be processed
    :type cycle: ICFGWTOCycle
    """
    def handleICFGCycle(self, cycle: ICFGWTOCycle):
        head = cycle.head.node
        increasing = True
        iteration = 0
        widen_delay = self.widen_delay  # Use class member for widen delay

        while True:
            # Get the abstract state of the cycle head 
            # pre_iteration_as is the postAbsTrace[head] of the cycle head before the current iteration
            # cur_iteration_as is the postAbsTrace[head] of the cycle head at the current iteration
            pre_iteration_as = self.post_abs_trace[head] if head in self.post_abs_trace else None
            self.handleICFGNode(head)  # Handle the cycle head node
            cur_iteration_as = self.post_abs_trace[head]

            if iteration >= widen_delay:
                if increasing:
                    # widening
                    self.post_abs_trace[head] = pre_iteration_as.widening(cur_iteration_as)
                    if self.post_abs_trace[head] == pre_iteration_as:
                        increasing = False
                        continue
                else:
                    # narrowing
                    self.post_abs_trace[head] = pre_iteration_as.narrowing(cur_iteration_as)
                    if self.post_abs_trace[head] == pre_iteration_as:
                        break

            # Handle the cycle components	
            for comp in cycle.components:
                if isinstance(comp, ICFGWTONode):
                    self.handleICFGNode(comp.node)
                elif isinstance(comp, ICFGWTOCycle):
                    # Handle the sub cycle (nested cycle)
                    self.handleICFGCycle(comp)

            iteration += 1

    def triggerUnderApproximation(self, start_node: pysvf.GlobalICFGNode, end_node: pysvf.CallICFGNode):
        # Do DFS to find the path from start_node to end_node, paths maybe multiple, we need to find all paths
        paths = []
        self.dfs(start_node, end_node, paths, [])
        # for each path, only print id
        for path in paths:
            path_str = ""
            for edge in path:
                assert isinstance(edge, pysvf.IntraCFGEdge)
                if edge.getCondition() is not None:
                    if edge.getSuccessorCondValue() == 0:
                        path_str += f"{edge.getSrcNode().getId()} -False-> {edge.getDstNode().getId()}, "
                    else:
                        path_str += f"{edge.getSrcNode().getId()} -True-> {edge.getDstNode().getId()}, "
                path_str += f"{edge.getSrcNode().getId()} -> {edge.getDstNode().getId()}, "
            print(path_str)

            # TODO: under approx interpret every statements



    def dfs(self, node: pysvf.ICFGNode, end_node: pysvf.ICFGNode, paths: List[List[pysvf.ICFGNode]], path: List[pysvf.ICFGNode]):
        if node == end_node:
            paths.append(path.copy())
            return
        for edge in node.getOutEdges():
            successor = edge.getDstNode()
            if successor not in path:
                path.append(edge)
                self.dfs(successor, end_node, paths, path)
                path.pop()
