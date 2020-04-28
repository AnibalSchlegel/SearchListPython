# -*- coding: utf-8 -*-
"""
SearchListPy

Created on Sun Apr 26 21:12:25 2020

@author: Anibal
"""

import sys

class Relation():

    def __init__(self, **kwargs):
        self._sourceNode = kwargs['source']
        self._targetNode = kwargs['target']
        self._cost = kwargs['cost']

    def SourceNode(self):
        return self._sourceNode
    
    def TargetNode(self):
        return self._targetNode
    
    def Cost(self):
        return self._cost
    
    def Clone(self):
        return Relation(source=self._sourceNode, target=self._targetNode, cost=self._cost)
    
    def InverseEquals(self, relation):
        return self._sourceNode.Name() == relation.TargetNode().Name() and self._targetNode.Name() == relation.SourceNode().Name()
    
    def IsEquals(self, relation):
        return self._sourceNode.Name() == relation.SourceNode().Name() and self._targetNode.Name() == relation.TargetNode().Name()
    
    def GetInverse(self):
        return Relation(source=self._targetNode, target=self._sourceNode, cost=self._cost)
    
    def __str__(self):
        return f'{self._sourceNode.Name()}->{self._targetNode.Name()} ({self._cost})'
    
class Node():

    def __init__(self, **kwargs):
        self._name = kwargs['name']
        self._weight = kwargs['weight'] if 'weight' in kwargs else 0
        self._totalWeight = kwargs['totalWeight'] if 'totalWeight' in kwargs else 0
    
    def Name(self):
        return self._name
    
    def Weight(self, value = None):
        if value:
            self._weight = value
        else: 
            return self._weight
        
    def TotalWeight(self, value = None):
        if value:
            self._totalWeight = value
        else: 
            return self._totalWeight

    def Clone(self):
        return Node(name=self._name, weight = self._weight, totalWeight=self._totalWeight)
    
    def __str__(self):
        return f'{self._name} {self._weight} {self._totalWeight}'

class SearchList():
    
    def __init__(self, **kwargs):
        
        def buildSearchTree(self, relation):
            if relation.TargetNode().Name() != self._startNode and relation.SourceNode().Name() != self._endNode:
                                             
                if not self._searchTree.get(relation.SourceNode().Name()):
                    self._searchTree[relation.SourceNode().Name()] = list()
                    
                if not self._searchTree.get(relation.TargetNode().Name()):
                    self._searchTree[relation.TargetNode().Name()] = list()
                
                self._searchTree[relation.SourceNode().Name()].append(relation)
        
        self._startNode = kwargs['start']
        self._endNode = kwargs['end']
        self._relations = kwargs['relations']
        self._searchTree = dict()
        self._openList = list()
        self._closedList = list()
        
        twoWays = kwargs['twoWays'] if 'twoWays' in kwargs else True
    
        for i in self._relations:
            buildSearchTree(self, i)
           
            if twoWays:
                inv = i.GetInverse()
                buildSearchTree(self, inv)

    def Run(self):
        
        def NotFinished(self):
            
            for i in self._closedList:
                if self._endNode == i.TargetNode().Name():
                    return False
            
            return True

        def UpdateOpenList(self, newNodes):
            
            for i in newNodes:
                updated = False
                
                for j in self._openList[::-1]:
                    if i.TargetNode().Name() == j.TargetNode().Name():
                        if i.TargetNode().TotalWeight() < j.TargetNode().TotalWeight():
                            self._openList[self._openList.index(j)] = i
                            updated = True
                        break
                
                if not updated:
                    self._openList.append(i)
        
        def UpdateClosedList(self, lowest):
            
            for i in self._closedList:
                if i.TargetNode().Name() == lowest.TargetNode().Name():
                    if i.TargetNode().TotalWeight() > lowest.TargetNode().TotalWeight():
                        self._closedList[self._closedList.index(i)] = lowest.Clone()
                    return
            
            self._closedList.append(lowest.Clone())
        
        def BuildPath(self):
            
            if len(self._closedList) == 0:
                return list()
            
            final = list()
            
            last = FindLastNodeInPath(self)
            
            if last:
                final.append(last)
                
                if last.SourceNode().Name() == self._startNode:
                    return final
                
                self._closedList.remove(last)
                
                for i in self._closedList[::-1]:
                    if final[len(final)-1].SourceNode().Name() == i.TargetNode().Name():
                        final.append(i)
                        
                return reversed(final)                                 
            
            return list()
            
        def FindLastNodeInPath(self):
            
            minWeight = sys.maxsize
            relation = None
            
            for i in self._closedList:
                if i.TargetNode().Name() == self._endNode and i.TargetNode().TotalWeight() < minWeight:
                    minWeight = i.TargetNode().TotalWeight()
                    relation = i
            
            return relation

        def ExtractLowestWeightedNode(self):
            
            minWeight = sys.maxsize
            relation = None
            
            for i in self._openList:
                if i.TargetNode().TotalWeight() < minWeight:
                    minWeight = i.TargetNode().TotalWeight()
                    relation = i

            if relation:
                cloned = relation.Clone()
                self._openList.remove(relation)
                return cloned
            
            return None

        def GetNextOpenNodes(self, lastClosed):
            
            newOpens = list()
            
            if lastClosed:
                relation = None
                                
                for i in self._searchTree[lastClosed.Name()]:
                    relation = i.Clone()
                                       
                    if any(x.InverseEquals(relation) for x in self._closedList) or any(x.IsEquals(relation) for x in self._openList):
                        continue
                                   
                    relation.TargetNode().Weight(relation.Cost())
                    relation.TargetNode().TotalWeight(relation.TargetNode().Weight() + lastClosed.TotalWeight())
                    newOpens.append(relation)

            return newOpens
        
        self._openList = list()
        self._closedList = list()
        lowestWeight = None
        relation = None
        lastClosed = None
            
        for i in self._searchTree[self._startNode]:
            relation = i.Clone()
            relation.TargetNode().Weight(relation.Cost())
            relation.TargetNode().TotalWeight(relation.TargetNode().Weight())
            self._openList.append(relation)

        while NotFinished(self):
            UpdateOpenList(self, GetNextOpenNodes(self, lastClosed))
            lowestWeight = ExtractLowestWeightedNode(self)
            UpdateClosedList(self, lowestWeight)
            lastClosed = lowestWeight.TargetNode()
                
        return BuildPath(self)      

def main():
    
    rels = [        
        Relation(source=Node(name='A'), target=Node(name='B'), cost=2),
        Relation(source=Node(name='A'), target=Node(name='C'), cost=3),
        Relation(source=Node(name='A'), target=Node(name='G'), cost=10),
        Relation(source=Node(name='B'), target=Node(name='D'), cost=2),
        Relation(source=Node(name='B'), target=Node(name='E'), cost=3),
        Relation(source=Node(name='C'), target=Node(name='E'), cost=2),
        Relation(source=Node(name='C'), target=Node(name='F'), cost=3),
        Relation(source=Node(name='C'), target=Node(name='G'), cost=5),
        Relation(source=Node(name='D'), target=Node(name='E'), cost=1),
        Relation(source=Node(name='D'), target=Node(name='H'), cost=4),
        Relation(source=Node(name='E'), target=Node(name='H'), cost=3),
        Relation(source=Node(name='E'), target=Node(name='I'), cost=4),       
        Relation(source=Node(name='F'), target=Node(name='G'), cost=1),
        Relation(source=Node(name='F'), target=Node(name='I'), cost=5),
        Relation(source=Node(name='F'), target=Node(name='J'), cost=3),
        Relation(source=Node(name='G'), target=Node(name='J'), cost=2),
        Relation(source=Node(name='G'), target=Node(name='N'), cost=3),
        Relation(source=Node(name='H'), target=Node(name='K'), cost=2),
        Relation(source=Node(name='H'), target=Node(name='L'), cost=3),
        Relation(source=Node(name='I'), target=Node(name='L'), cost=2),
        Relation(source=Node(name='I'), target=Node(name='M'), cost=3),
        Relation(source=Node(name='J'), target=Node(name='M'), cost=2),
        Relation(source=Node(name='J'), target=Node(name='N'), cost=3),
        Relation(source=Node(name='N'), target=Node(name='M'), cost=2),
        Relation(source=Node(name='K'), target=Node(name='L'), cost=4),
        Relation(source=Node(name='K'), target=Node(name='O'), cost=5),
        Relation(source=Node(name='L'), target=Node(name='O'), cost=1),
        Relation(source=Node(name='M'), target=Node(name='O'), cost=2)
    ]
    
    result = SearchList(start='B', end='O', relations=rels).Run()
    
    total = 0
    
    if result:
        for i in result:
            total += i.Cost()
            print(i)
        print(f'Total: {total}')
    else:
        print('something went wrong')
    
if __name__ == '__main__': main()
