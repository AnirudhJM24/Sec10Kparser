import sec_parser as sp
from sec_parser.processing_steps import TopSectionManagerFor10Q, IndividualSemanticElementExtractor, TopSectionTitleCheck
from sec_parser import Edgar10QParser
from sec_parser.processing_steps import AbstractProcessingStep
from sec_parser.semantic_elements import (
    TextElement,
    TableElement,
    TitleElement,
    TopSectionTitle,
    )
from sec_parser.processing_steps import TitleClassifier,TextClassifier
from sec_parser.semantic_tree import AlwaysNestAsParentRule, NestSameTypeDependingOnLevelRule
from collections import deque


class ItemElement(sp.TitleElement):
    pass


# Create a custom parsing step
class MyClassifier(TitleClassifier):
    def _process_element(self, element, context):
        if 'item' in element.text.lower():
            return ItemElement.create_from_element(element, log_origin="MyClassifier")

        # Let the parent class handle the other cases
        return super()._process_element(element, context)

class tenkparser:

    elements = []




    def without_10q_related_steps(self):
        all_steps = sp.Edgar10QParser().get_default_steps()
        
        # Change 1: Remove the TopSectionManagerFor10Q
        steps_without_top_section_manager = [step for step in all_steps if not isinstance(step, TopSectionManagerFor10Q)]
        steps_without_top_section_manager.insert(12,MyClassifier(types_to_process={sp.TitleElement}))
        
        # Change 2: Replace the IndividualSemanticElementExtractor with a new one that has the top section checks removed
        def get_checks_without_top_section_title_check():
            all_checks = sp.Edgar10QParser().get_default_single_element_checks()
            return [check for check in all_checks if not isinstance(check, TopSectionTitleCheck)]
        return [
            IndividualSemanticElementExtractor(get_checks=get_checks_without_top_section_title_check) 
            if isinstance(step, IndividualSemanticElementExtractor) 
            else step
            for step in steps_without_top_section_manager
        ]



    def nest_rules(self):

        return [
            AlwaysNestAsParentRule(ItemElement),AlwaysNestAsParentRule(TitleElement,exclude_children={ItemElement})]


    def section_bfs(self,treeNode):
        q = deque()
        nodes = []
        q.append(treeNode)

        nodestr = ''

        while q:

            item = q.popleft()

            nodestr += item.text +'\n'

            for child in item.children:

                q.append(child)
                
        
        return nodestr

    def dfs(self,treenode, nodestr='', visited=None):
        if visited is None:
            visited = set()
        visited.add(treenode)

        nodestr += str(treenode.get_source_code())

        for neighbor in treenode.children:
            if neighbor not in visited:
                nodestr = self.dfs(neighbor, nodestr, visited)
        return nodestr
    
    def parse10K(self,filename):

        parser = Edgar10QParser(self.without_10q_related_steps)

        with open(filename) as file:

            elements = parser.parse(file)

        self.tree = sp.TreeBuilder(self.nest_rules).build(elements)
        print(sp.render(self.tree))
        return sp.render(self.tree)
    
    def getitems(self):

        self.itemnodes = []

        for node in self.tree:

            if isinstance(node.semantic_element, ItemElement):

                self.itemnodes.append(node.semantic_element.text)
        
        print(self.itemnodes)
        return self.itemnodes
    
    def getsegmenthtml(self,item):

        htmlstr = ''

        for node in self.tree:

            if item in node.semantic_element.text:

                htmlstr = self.dfs(node)
        
        return htmlstr





    



