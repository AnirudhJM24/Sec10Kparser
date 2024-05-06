import os
from bs4 import BeautifulSoup
import pandas as pd
from collections import deque
from sec_downloader import Downloader
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


class ItemElement(sp.TitleElement):
    pass


# Create a custom parsing step
class MyClassifier(TitleClassifier):
    def _process_element(self, element, context):
        if 'item' in element.text.lower():
            return ItemElement.create_from_element(element, log_origin="MyClassifier")

        # Let the parent class handle the other cases
        return super()._process_element(element, context)



def without_10q_related_steps():
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



def nest_rules():

    return [
        AlwaysNestAsParentRule(ItemElement),AlwaysNestAsParentRule(TitleElement,exclude_children={ItemElement})]


def section_bfs(treeNode):
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

def dfs(treenode, nodestr='', visited=None):
    if visited is None:
        visited = set()
    visited.add(treenode)

    if 'Table of Contents' not in treenode.text:
        nodestr += treenode.text + '\n'

    for neighbor in treenode.children:
        if neighbor not in visited:
            nodestr = dfs(neighbor, nodestr, visited)
    return nodestr


def find_html_files(folder_path):
    html_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files


def analyze():
    folder_path = '10Kdata\sec-edgar-filings'
    html_files = find_html_files(folder_path)
    print("HTML Files found in the folder and its subdirectories:")
    parser = Edgar10QParser(without_10q_related_steps)

    for file in html_files[:1]:
        print(file)


        #path = r'10Kdata\sec-edgar-filings\GOOG\10-K\0001652044-20-000008\primary-document.html'

        with open(file) as f:
            elements = parser.parse(f)
    
        tree = sp.TreeBuilder(nest_rules).build(elements)

        for nodes in tree:

            if isinstance(nodes.semantic_element,ItemElement):

                if "discussion" in nodes.semantic_element.text.lower():

                    print(sp.render(nodes))
                    result = dfs(nodes)
                    #print(result)

        output = sp.render(tree,char_display_limit=100)

        print(output)
    return result

    

            



