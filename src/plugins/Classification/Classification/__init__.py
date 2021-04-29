"""
This is where the implementation of the plugin code goes.
The Classification-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('Classification')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Classification(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        META = self.META
        active_node = self.active_node

        places = []
        placesPaths = []
        transitions = []
        transitionPaths = []
        arcs = []

        #Collect all nodes
        nodes = core.load_sub_tree(active_node)

        #Separate nodes into types
        for node in nodes:
            if core.get_attribute(node, 'name') in ("Place-Transition", "Transition-Place"):
                arcs.append(node)
            elif core.get_attribute(node, 'name') in ("Transition"):
                transitions.append(node)
            elif core.get_attribute(node, 'name') in ("Place"):
                places.append(node)

        #Add transition paths to an array
        for transition in transitions:
                transitionPaths.append(core.get_path(transition))
        
        #Add place paths to an array
        for place in places:
                placesPaths.append(core.get_path(place))

        def isStateMachine():
            #Check if any Transitions dst is listed twice
            for path in transitionPaths:
                inplaceCt = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'dst'):
                        inplaceCt = inplaceCt + 1
                if inplaceCt > 1:
                    return False

            #Check if any Transitions src is listed twice
            for path in transitionPaths:
                outplaceCt = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'src'):
                        outplaceCt = outplaceCt + 1
                if outplaceCt > 1:
                    return False
            
            return True

        def isMarkedGraph():
            #Check that every Place is listed exactly once as a Dst
            for path in placesPaths:
                inplaceCt = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'dst'):
                        inplaceCt = inplaceCt + 1
                if inplaceCt != 1:
                    return False

            #Check that every Place is listed exactly once as a Src
            for path in placesPaths:
                inplaceCt = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'src'):
                        inplaceCt = inplaceCt + 1
                if inplaceCt != 1:
                    return False  

            return True

        def isFreeChoice():
            #Check if any Transition dst is listed twice
            for path in transitionPaths:
                inplaceCt = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'dst'):
                        inplaceCt = inplaceCt + 1
                if inplaceCt > 1:
                    return False   
            return True

        def isWorkflowNet():
            nodeSrc = {}
            #Check if there is a start node (Place node without an incoming arc)
            for path in placesPaths:
                inplaceCt = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'dst'):
                        inplaceCt = inplaceCt + 1
                nodeSrc[path] = inplaceCt


            val_list = list(nodeSrc.values())

            #Fail if there is more than 1 start node
            if val_list.count(0)>1:
                return False

            # position = val_list.index(0)
            # key_list = list(nodeSrc.keys())

            # startNode = key_list[position]

            #Check if there is an end node (Place node without an outgoing arc
            for path in placesPaths:
                inplaceCt = 0
                for arc in arcs:
                    if path == core.get_pointer_path(arc, 'src'):
                        inplaceCt = inplaceCt + 1
                nodeSrc[path] = inplaceCt

            val_list = list(nodeSrc.values())

            #Fail if there is more than 1 end node
            if val_list.count(0)>1:
                return False

            # position = val_list.index(0)
            # key_list = list(nodeSrc.keys())

            # endNode = key_list[position]

            return True
        

        StateMachineResult = isStateMachine()
        FreeChoiceResult = isFreeChoice()
        MarkedGraphResult = isMarkedGraph()
        WorkflowNetResult = isWorkflowNet()

        self.send_notification(f"StateMachine - {StateMachineResult}")
        self.send_notification(f"Free Choice - {FreeChoiceResult}")
        self.send_notification(f"Marked Graph - {MarkedGraphResult}")
        self.send_notification(f"Workflow Net - {WorkflowNetResult}")