"""
Knowledge Management System - 5-Floor Library Architecture
Handles knowledge indexing, search, and retrieval for personal knowledge bases
"""

import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime


class LibrarySystem:
    """
    Manages knowledge graph and file indexing for 5-floor architecture
    Provides search and retrieval across your personal knowledge base
    """

    def __init__(self, knowledge_graph_path: str, floor_mapping_path: str):
        """
        Initialize library system with knowledge graph and floor mapping
        
        Args:
            knowledge_graph_path: Path to knowledge_graph.json
            floor_mapping_path: Path to floor_mapping.md
        """
        self.knowledge_graph = self._load_json(knowledge_graph_path)
        self.floor_mapping_path = floor_mapping_path
        self.query_history = []
        self.session_start = datetime.now()

    @staticmethod
    def _load_json(path: str) -> Dict:
        """Load JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Could not find {path}")
            return {}

    def search_by_concept(self, concept: str) -> List[Dict]:
        """
        Search knowledge graph for files related to a concept
        
        Args:
            concept: Search term (e.g., "career advancement", "strategy")
            
        Returns:
            List of file references with metadata
        """
        matching_nodes = self._search_knowledge_graph(concept.lower())
        
        if not matching_nodes:
            return []
        
        files_found = self._extract_files_from_nodes(matching_nodes)
        
        self._log_query('concept', concept, len(files_found))
        
        return files_found

    def search_by_floor(self, floor_number: int) -> List[Dict]:
        """
        Retrieve all files on a specific floor
        
        Args:
            floor_number: Floor number (1-5)
            
        Returns:
            List of file references on that floor
        """
        floors = {
            1: "Foundation & Navigation",
            2: "Frameworks & Understanding",
            3: "Networks & Relationships",
            4: "Action & Implementation",
            5: "Vision & Meaning"
        }
        
        if floor_number not in floors:
            return []
        
        files_on_floor = self._get_files_by_floor(floor_number)
        
        self._log_query('floor', f"Floor {floor_number}", len(files_on_floor))
        
        return files_on_floor

    def search_by_tag(self, tag: str) -> List[Dict]:
        """
        Search for files by tag/category
        
        Args:
            tag: Tag to search for (e.g., "career", "strategy", "daily")
            
        Returns:
            List of matching files
        """
        tag_mapping = {
            "career": ["01_Career_Master.md", "02_Skills_Inventory.md"],
            "strategy": ["35_Strategic_Plan.md"],
            "daily": ["03_Daily_Operations.md"],
            "frameworks": ["32_Personality_Framework.md"],
            "network": ["18_Network_Map.md"],
            "investigation": ["06_Project_Template.md", "26_Decision_Tree.md"],
        }
        
        matching_tag = tag.lower()
        files = []
        
        for key, file_list in tag_mapping.items():
            if matching_tag in key:
                files.extend([{"name": f, "tag": key} for f in file_list])
        
        self._log_query('tag', tag, len(files))
        
        return files

    def get_related_concepts(self, concept: str, max_hops: int = 2) -> List[Dict]:
        """
        Find concepts related to a starting concept
        
        Args:
            concept: Starting concept
            max_hops: Maximum connection depth to traverse
            
        Returns:
            List of related concepts with their connections
        """
        current_node = concept.lower()
        visited = set()
        related = []
        
        for hop in range(max_hops):
            if current_node in visited:
                break
                
            visited.add(current_node)
            connections = self._get_connections(current_node)
            
            if connections:
                related.extend(connections)
                current_node = connections[0]['label'].lower()
        
        self._log_query('related_concepts', concept, len(related))
        
        return related

    def get_query_history(self) -> List[Dict]:
        """
        Get all queries from current session
        
        Returns:
            List of query records with timestamps
        """
        return self.query_history

    def get_session_summary(self) -> Dict:
        """
        Generate summary statistics for current session
        
        Returns:
            Dictionary with query counts by type
        """
        if not self.query_history:
            return {"total_queries": 0, "by_type": {}}
        
        by_type = {}
        for entry in self.query_history:
            qtype = entry['query_type']
            by_type[qtype] = by_type.get(qtype, 0) + 1
        
        return {
            "session_start": self.session_start.isoformat(),
            "total_queries": len(self.query_history),
            "by_type": by_type
        }

    # ===== INTERNAL HELPER METHODS =====

    def _search_knowledge_graph(self, concept: str) -> List[Dict]:
        """Find nodes in knowledge graph matching search term"""
        graph = self.knowledge_graph.get('knowledge_graph', {})
        nodes = graph.get('nodes', {})
        
        matching = []
        for node_id, node_data in nodes.items():
            label = node_data.get('label', '').lower()
            if concept in label or concept in node_id.lower():
                matching.append(node_data)
        
        return matching

    def _extract_files_from_nodes(self, nodes: List[Dict]) -> List[Dict]:
        """Extract file references from concept nodes"""
        files = []
        for node in nodes:
            file_locs = node.get('file_locations', [])
            for loc in file_locs:
                files.append({
                    "name": loc,
                    "concept": node.get('label'),
                    "floor": node.get('floor')
                })
        return files

    def _get_files_by_floor(self, floor: int) -> List[Dict]:
        """Get all files assigned to a specific floor"""
        floor_files = {
            1: ["00_Hub_Index.md", "01_Career_Master.md", "02_Skills_Inventory.md", 
                "03_Daily_Operations.md"],
            2: ["10_Glossary.md", "11_Transmittal_Standards.md"],
            3: ["18_Network_Map.md", "21_Background_Story.md"],
            4: ["06_Project_Template.md", "26_Decision_Tree.md"],
            5: ["32_Personality_Framework.md", "35_Strategic_Plan.md"],
        }
        
        files = floor_files.get(floor, [])
        return [{"name": f, "floor": floor} for f in files]

    def _get_connections(self, node_id: str) -> List[Dict]:
        """Get connected concepts for a given node"""
        graph = self.knowledge_graph.get('knowledge_graph', {})
        nodes = graph.get('nodes', {})
        
        if node_id not in nodes:
            return []
        
        node = nodes[node_id]
        connections = node.get('connects_to', [])
        
        connected_nodes = []
        for conn_id in connections:
            if conn_id in nodes:
                connected = nodes[conn_id]
                connected_nodes.append({
                    'id': conn_id,
                    'label': connected.get('label', conn_id),
                    'files': connected.get('file_locations', [])
                })
        
        return connected_nodes

    def _log_query(self, query_type: str, query: str, results_count: int):
        """Log query for session history"""
        self.query_history.append({
            'timestamp': datetime.now().isoformat(),
            'query_type': query_type,
            'query': query,
            'results_count': results_count
        })


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    # Initialize the library system
    library = LibrarySystem(
        knowledge_graph_path="knowledge_graph.json",
        floor_mapping_path="floor_mapping.md"
    )
    
    # Example 1: Search by concept
    print("=== Search by Concept ===")
    files = library.search_by_concept("career advancement")
    print(f"Found {len(files)} files:")
    for f in files:
        print(f"  - {f['name']} (Floor {f.get('floor', 'N/A')})")
    print()
    
    # Example 2: Search by floor
    print("=== Search by Floor ===")
    files = library.search_by_floor(3)
    print(f"Floor 3 contains {len(files)} files:")
    for f in files:
        print(f"  - {f['name']}")
    print()
    
    # Example 3: Search by tag
    print("=== Search by Tag ===")
    files = library.search_by_tag("strategy")
    print(f"Strategy-related files: {len(files)}")
    for f in files:
        print(f"  - {f['name']}")
    print()
    
    # Example 4: Find related concepts
    print("=== Find Related Concepts ===")
    related = library.get_related_concepts("career", max_hops=2)
    print(f"Concepts related to 'career': {len(related)}")
    for r in related[:3]:
        print(f"  - {r['label']}")
    print()
    
    # Example 5: Session summary
    print("=== Session Summary ===")
    summary = library.get_session_summary()
    print(f"Total queries: {summary['total_queries']}")
    print("By type:")
    for qtype, count in summary['by_type'].items():
        print(f"  - {qtype}: {count}")
