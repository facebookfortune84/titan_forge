"""
TitanForge File Manifest & Knowledge Graph Integration
Provides file hashing, provenance tracking, and agent awareness.
Uses SHA-256 for file integrity and creates knowledge graph nodes for NeuralLattice.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class FileManifest:
    """Generate cryptographic manifest of project files for agent awareness."""
    
    def __init__(self, root_path: str = "F:/TitanForge"):
        self.root_path = Path(root_path)
        self.manifest = {}
        self.knowledge_graph = []
    
    @staticmethod
    def sha256_file(filepath: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def add_file(self, filepath: Path, file_type: str, purpose: str, 
                 dependencies: Optional[List[str]] = None) -> Dict:
        """Add a file to manifest with metadata."""
        try:
            file_hash = self.sha256_file(filepath)
            file_size = filepath.stat().st_size
            file_mtime = datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            
            entry = {
                "path": str(filepath),
                "relative_path": str(filepath.relative_to(self.root_path)),
                "hash_sha256": file_hash,
                "size_bytes": file_size,
                "type": file_type,
                "purpose": purpose,
                "dependencies": dependencies or [],
                "last_modified": file_mtime,
                "status": "verified"
            }
            
            # Add to manifest keyed by relative path
            rel_path = str(filepath.relative_to(self.root_path)).replace("\\", "/")
            self.manifest[rel_path] = entry
            
            # Create knowledge graph node
            self._create_graph_node(entry)
            
            return entry
        except FileNotFoundError:
            return {"error": f"File not found: {filepath}"}
    
    def _create_graph_node(self, file_entry: Dict) -> Dict:
        """Create knowledge graph node for agent awareness."""
        node = {
            "type": "FILE_NODE",
            "id": f"file_{hash(file_entry['path'])}",
            "name": Path(file_entry['path']).name,
            "attributes": {
                "full_path": file_entry["path"],
                "relative_path": file_entry["relative_path"],
                "hash": file_entry["hash_sha256"],
                "file_type": file_entry["type"],
                "purpose": file_entry["purpose"],
                "size_bytes": file_entry["size_bytes"],
                "last_modified": file_entry["last_modified"]
            },
            "relationships": {
                "depends_on": [
                    {"type": "FILE_NODE", "ref": dep}
                    for dep in file_entry.get("dependencies", [])
                ]
            }
        }
        self.knowledge_graph.append(node)
        return node
    
    def generate_manifest(self, output_path: Optional[str] = None) -> str:
        """Generate JSON manifest for storage/ingestion."""
        manifest_json = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "root_path": str(self.root_path),
            "file_count": len(self.manifest),
            "files": self.manifest
        }
        
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(manifest_json, f, indent=2)
            print(f"✓ Manifest saved to {output_file}")
        
        return json.dumps(manifest_json, indent=2)
    
    def generate_knowledge_graph(self, output_path: Optional[str] = None) -> str:
        """Generate knowledge graph for NeuralLattice ingestion."""
        graph_json = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "graph_type": "file_dependency_graph",
            "nodes": self.knowledge_graph,
            "metadata": {
                "total_nodes": len(self.knowledge_graph),
                "graph_density": self._calculate_graph_density()
            }
        }
        
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(graph_json, f, indent=2)
            print(f"✓ Knowledge graph saved to {output_file}")
        
        return json.dumps(graph_json, indent=2)
    
    def _calculate_graph_density(self) -> float:
        """Calculate graph density metric."""
        if not self.knowledge_graph:
            return 0.0
        
        total_relationships = sum(
            len(node.get("relationships", {}).get("depends_on", []))
            for node in self.knowledge_graph
        )
        
        n = len(self.knowledge_graph)
        max_relationships = n * (n - 1)
        
        return total_relationships / max_relationships if max_relationships > 0 else 0.0
    
    def export_for_agent_context(self, output_path: Optional[str] = None) -> Dict:
        """Export manifest in format suitable for agent context injection."""
        agent_context = {
            "system_metadata": {
                "project_name": "TitanForge",
                "description": "AI-powered multi-agent software development agency",
                "version": "1.0.0",
                "generated_at": datetime.now().isoformat()
            },
            "file_inventory": {
                "core_system": self._categorize_files("core"),
                "api_endpoints": self._categorize_files("api"),
                "frontend": self._categorize_files("frontend"),
                "agents": self._categorize_files("agents"),
                "tests": self._categorize_files("tests"),
                "scripts": self._categorize_files("scripts"),
                "documentation": self._categorize_files("docs")
            },
            "dependency_graph": self.knowledge_graph
        }
        
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(agent_context, f, indent=2)
            print(f"✓ Agent context saved to {output_file}")
        
        return agent_context
    
    def _categorize_files(self, category: str) -> List[Dict]:
        """Extract files matching a category."""
        category_keywords = {
            "core": ["main.py", "app.py", "__init__.py"],
            "api": ["api/v1/", "router", "endpoint"],
            "frontend": ["src/", "tsx", "jsx"],
            "agents": ["swarm/", "agent"],
            "tests": ["test_", "tests/"],
            "scripts": ["scripts/", ".ps1"],
            "docs": ["docs/", ".md"]
        }
        
        matching_files = []
        for filepath, entry in self.manifest.items():
            keywords = category_keywords.get(category, [])
            if any(kw.lower() in filepath.lower() for kw in keywords):
                matching_files.append(entry)
        
        return matching_files


def scan_and_hash_project(root_path: str = "F:/TitanForge") -> tuple:
    """Scan entire project and generate manifests."""
    manifest = FileManifest(root_path)
    
    # Core system files
    manifest.add_file(
        Path(root_path) / "titanforge_backend/app/main.py",
        "python",
        "Central FastAPI application and router registration",
        ["app/api/v1/*", "core/config.py", "database.py"]
    )
    
    # API Endpoints
    api_files = [
        ("app/api/v1/auth.py", "Authentication endpoints (register, login, JWT)"),
        ("app/api/v1/dashboard.py", "Dashboard stats and metrics"),
        ("app/api/v1/pricing.py", "Pricing tier management"),
        ("app/api/v1/sales_funnel.py", "Sales funnel and lead magnet"),
        ("app/api/v1/roi_calculator.py", "ROI PDF generation"),
        ("app/api/v1/blog.py", "Blog system"),
        ("app/api/v1/leads.py", "Lead capture and management"),
        ("app/api/v1/agents.py", "Agent management endpoints"),
    ]
    
    for file, purpose in api_files:
        filepath = Path(root_path) / f"titanforge_backend/{file}"
        if filepath.exists():
            manifest.add_file(filepath, "python", purpose, ["schemas.py", "crud.py"])
    
    # Frontend components
    frontend_files = [
        ("src/App.tsx", "Root application component and routing"),
        ("src/LandingPageProPro.tsx", "Professional landing page with metrics"),
        ("src/AgentCockpitPro.tsx", "Agent control interface (multi-modal)"),
        ("src/RegisterPage.tsx", "User registration form"),
        ("src/LoginPage.tsx", "User login form"),
        ("src/PricingPage.tsx", "Pricing page with tier cards"),
    ]
    
    for file, purpose in frontend_files:
        filepath = Path(root_path) / f"frontend/{file}"
        if filepath.exists():
            manifest.add_file(filepath, "typescript", purpose, ["components/*", "services/*"])
    
    # Test files
    test_files = [
        ("tests/endpoints/test_all_endpoints.py", "API endpoint validation"),
        ("tests/integration/test_complete_journey.py", "End-to-end journey testing"),
        ("tests/integration/test_comprehensive_integration.py", "Comprehensive integration tests"),
    ]
    
    for file, purpose in test_files:
        filepath = Path(root_path) / file
        if filepath.exists():
            manifest.add_file(filepath, "python", purpose, ["titanforge_backend/app/*"])
    
    # Generate outputs
    docs_path = Path(root_path) / "docs"
    docs_path.mkdir(exist_ok=True)
    
    manifest_json = manifest.generate_manifest(
        str(docs_path / "FILE_MANIFEST.json")
    )
    
    graph_json = manifest.generate_knowledge_graph(
        str(docs_path / "KNOWLEDGE_GRAPH.json")
    )
    
    agent_context = manifest.export_for_agent_context(
        str(docs_path / "AGENT_CONTEXT.json")
    )
    
    return manifest, agent_context


if __name__ == "__main__":
    print("\n🔐 TitanForge File Manifest Generator")
    print("=" * 50)
    manifest, context = scan_and_hash_project()
    print("\n✓ File hashing and knowledge graph generation complete!")
    print(f"✓ Generated manifest for {len(manifest.manifest)} files")
    print(f"✓ Created {len(manifest.knowledge_graph)} knowledge graph nodes")
    print("\nOutputs:")
    print("  - docs/FILE_MANIFEST.json (file hashes & metadata)")
    print("  - docs/KNOWLEDGE_GRAPH.json (agent awareness graph)")
    print("  - docs/AGENT_CONTEXT.json (agent system context)")
