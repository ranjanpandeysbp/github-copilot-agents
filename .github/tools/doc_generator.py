#!/usr/bin/env python3
"""
Comprehensive Documentation Generator for Java Repositories
Analyzes Java code repositories and generates detailed technical documentation with diagrams.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass


@dataclass
class JavaClass:
    name: str
    package: str
    path: str
    is_entity: bool = False
    is_dto: bool = False
    is_service: bool = False
    is_controller: bool = False
    is_repository: bool = False
    is_exception: bool = False
    fields: List[str] = None
    methods: List[str] = None
    dependencies: Set[str] = None
    annotations: List[str] = None

    def __post_init__(self):
        if self.fields is None:
            self.fields = []
        if self.methods is None:
            self.methods = []
        if self.dependencies is None:
            self.dependencies = set()
        if self.annotations is None:
            self.annotations = []

    @property
    def full_name(self) -> str:
        return f"{self.package}.{self.name}"

    @property
    def type_label(self) -> str:
        if self.is_entity:
            return "Entity"
        elif self.is_dto:
            return "DTO"
        elif self.is_service:
            return "Service"
        elif self.is_controller:
            return "Controller"
        elif self.is_repository:
            return "Repository"
        elif self.is_exception:
            return "Exception"
        return "Class"


class JavaCodeAnalyzer:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.java_files: List[Path] = []
        self.classes: Dict[str, JavaClass] = {}
        self.project_name = repo_path.name
        self.tech_stack: Set[str] = set()
        self.pom_file = repo_path / "pom.xml"
        self.read_me = repo_path / "README.md"

    def discover_java_files(self) -> None:
        """Find all Java files in the repository."""
        for java_file in self.repo_path.rglob("*.java"):
            # Skip test files for now
            if "test" not in str(java_file).lower():
                self.java_files.append(java_file)

    def extract_package(self, content: str) -> Optional[str]:
        """Extract package declaration from Java file."""
        match = re.search(r'package\s+([a-zA-Z0-9_.]+)\s*;', content)
        return match.group(1) if match else None

    def extract_class_name(self, content: str) -> Optional[str]:
        """Extract class name from Java file."""
        # Look for class or interface declaration
        match = re.search(r'(?:public\s+)?(?:class|interface|enum|record)\s+([a-zA-Z0-9_]+)', content)
        return match.group(1) if match else None

    def extract_annotations(self, content: str) -> List[str]:
        """Extract Spring and other annotations."""
        annotations = re.findall(r'@([A-Z][a-zA-Z0-9]*)', content)
        return list(set(annotations))

    def extract_fields(self, content: str) -> List[str]:
        """Extract field declarations."""
        # Simple regex to find field declarations
        lines = content.split('\n')
        fields = []
        for line in lines:
            if re.search(r'(private|protected|public)\s+\w+\s+\w+', line):
                field = re.search(r'(\w+)\s+(\w+)\s*[=;]', line)
                if field:
                    fields.append(f"{field.group(1)} {field.group(2)}")
        return fields

    def extract_methods(self, content: str) -> List[str]:
        """Extract method signatures."""
        methods = re.findall(r'(?:public|private|protected)\s+(?:static\s+)?(?:\w+\s+)*(\w+)\s*\([^)]*\)', content)
        return list(set(methods))

    def extract_dependencies(self, content: str) -> Set[str]:
        """Extract class dependencies from imports and field types."""
        dependencies = set()
        imports = re.findall(r'import\s+(?:static\s+)?(?:[\w.]+\.)?(\w+)\s*;', content)
        dependencies.update(imports)
        # Also find field type references
        types = re.findall(r'(?:private|protected|public)\s+([A-Z]\w+)[\s<]', content)
        dependencies.update(types)
        return dependencies

    def analyze_java_file(self, java_file: Path) -> Optional[JavaClass]:
        """Analyze a single Java file."""
        try:
            content = java_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {java_file}: {e}")
            return None

        package = self.extract_package(content)
        class_name = self.extract_class_name(content)

        if not class_name or not package:
            return None

        # Determine class type based on naming and path
        relative_path = java_file.relative_to(self.repo_path)
        is_entity = "entity" in str(relative_path).lower() or class_name.endswith("Entity")
        is_dto = "dto" in str(relative_path).lower() or class_name.endswith("DTO") or class_name.endswith("Dto")
        is_service = "service" in str(relative_path).lower() or class_name.endswith("Service")
        is_controller = "controller" in str(relative_path).lower() or class_name.endswith("Controller")
        is_repository = "repository" in str(relative_path).lower() or "Repository" in class_name
        is_exception = "exception" in str(relative_path).lower() or class_name.endswith("Exception")

        java_class = JavaClass(
            name=class_name,
            package=package,
            path=str(relative_path),
            is_entity=is_entity,
            is_dto=is_dto,
            is_service=is_service,
            is_controller=is_controller,
            is_repository=is_repository,
            is_exception=is_exception,
            fields=self.extract_fields(content),
            methods=self.extract_methods(content),
            dependencies=self.extract_dependencies(content),
            annotations=self.extract_annotations(content)
        )

        return java_class

    def analyze_pom_xml(self) -> None:
        """Extract tech stack from pom.xml."""
        if not self.pom_file.exists():
            return

        try:
            content = self.pom_file.read_text(encoding='utf-8')
            # Extract version and key dependencies
            if "spring-boot" in content:
                version_match = re.search(r'<version>(3\.\d+\.\d+)</version>', content)
                if version_match:
                    self.tech_stack.add(f"Spring Boot {version_match.group(1)}")
                else:
                    self.tech_stack.add("Spring Boot")

            if "spring-boot-starter-web" in content:
                self.tech_stack.add("Spring Web")
            if "spring-boot-starter-data-jpa" in content:
                self.tech_stack.add("Spring Data JPA")
            if "mysql" in content:
                self.tech_stack.add("MySQL")
            if "h2database" in content:
                self.tech_stack.add("H2 Database")
            if "lombok" in content:
                self.tech_stack.add("Lombok")
            if "springdoc-openapi" in content:
                self.tech_stack.add("Swagger/OpenAPI")
            if "junit" in content or "spring-boot-starter-test" in content:
                self.tech_stack.add("JUnit")

            java_version_match = re.search(r'<java\.version>(\d+)</java\.version>', content)
            if java_version_match:
                self.tech_stack.add(f"Java {java_version_match.group(1)}")
        except Exception as e:
            print(f"Error reading pom.xml: {e}")

    def analyze(self) -> None:
        """Analyze all Java files in the repository."""
        self.discover_java_files()
        self.analyze_pom_xml()

        for java_file in self.java_files:
            java_class = self.analyze_java_file(java_file)
            if java_class:
                self.classes[java_class.full_name] = java_class


class DocumentationGenerator:
    def __init__(self, analyzer: JavaCodeAnalyzer):
        self.analyzer = analyzer
        self.doc_lines: List[str] = []

    def add_heading(self, text: str, level: int = 1) -> None:
        """Add a markdown heading."""
        self.doc_lines.append(f"{'#' * level} {text}\n")

    def add_paragraph(self, text: str) -> None:
        """Add a paragraph."""
        self.doc_lines.append(f"{text}\n")

    def add_code_block(self, code: str, language: str = "") -> None:
        """Add a code block."""
        self.doc_lines.append(f"```{language}\n{code}\n```\n")

    def add_mermaid_diagram(self, diagram: str, title: str = "") -> None:
        """Add a Mermaid diagram."""
        if title:
            self.doc_lines.append(f"**{title}**\n")
        self.doc_lines.append("```mermaid\n")
        self.doc_lines.append(diagram)
        self.doc_lines.append("\n```\n")

    def generate_architecture_overview(self) -> None:
        """Generate architecture overview."""
        self.add_heading("System Architecture Overview", 2)

        # Count classes by type
        entities = [c for c in self.analyzer.classes.values() if c.is_entity]
        dtos = [c for c in self.analyzer.classes.values() if c.is_dto]
        services = [c for c in self.analyzer.classes.values() if c.is_service]
        controllers = [c for c in self.analyzer.classes.values() if c.is_controller]
        repositories = [c for c in self.analyzer.classes.values() if c.is_repository]

        # Component overview
        overview = f"""
The {self.analyzer.project_name} project follows a layered architecture pattern with clear separation of concerns:

- **Controllers** ({len(controllers)}): Handle HTTP requests and responses
- **Services** ({len(services)}): Contain business logic and orchestrate operations
- **Repositories** ({len(repositories)}): Manage data access and persistence
- **Entities** ({len(entities)}): Represent database domain models
- **DTOs** ({len(dtos)}): Transfer data between layers
"""
        self.add_paragraph(overview)

    def generate_data_flow_diagram(self) -> None:
        """Generate data flow diagram."""
        self.add_heading("Data Flow Diagram", 2)

        diagram = """graph TD
    Client["🔹 Client/Browser"]
    Controller["🔹 REST Controller"]
    Service["🔹 Service Layer"]
    Repository["🔹 Repository"]
    DB["🗄️ Database"]
    
    Client -->|HTTP Request| Controller
    Controller -->|Method Call| Service
    Service -->|Data Query| Repository
    Repository -->|SQL Query| DB
    DB -->|Result Set| Repository
    Repository -->|Data Objects| Service
    Service -->|DTO| Controller
    Controller -->|JSON Response| Client
"""
        self.add_mermaid_diagram(diagram, "Client-Server Data Flow")

    def generate_component_diagram(self) -> None:
        """Generate component interaction diagram."""
        self.add_heading("Component Interaction Diagram", 2)

        entities = [c for c in self.analyzer.classes.values() if c.is_entity]
        services = [c for c in self.analyzer.classes.values() if c.is_service]
        controllers = [c for c in self.analyzer.classes.values() if c.is_controller]

        diagram_lines = ["graph TD"]

        # Add components
        diagram_lines.append('  subgraph "Presentation Layer"')
        for controller in controllers[:3]:  # Limit to top 3
            safe_name = controller.name.replace("-", "_")
            diagram_lines.append(f'    {safe_name}["{controller.name}"]')
        diagram_lines.append("  end")

        diagram_lines.append('  subgraph "Business Logic Layer"')
        for service in services[:3]:  # Limit to top 3
            safe_name = service.name.replace("-", "_")
            diagram_lines.append(f'    {safe_name}["{service.name}"]')
        diagram_lines.append("  end")

        diagram_lines.append('  subgraph "Data Layer"')
        for entity in entities[:3]:  # Limit to top 3
            safe_name = entity.name.replace("-", "_")
            diagram_lines.append(f'    {safe_name}["{entity.name}"]')
        diagram_lines.append("  end")

        diagram = "\n".join(diagram_lines)
        self.add_mermaid_diagram(diagram, "Layered Architecture Components")

    def generate_class_diagram(self) -> None:
        """Generate class diagram for key classes."""
        self.add_heading("Key Classes and Relationships", 2)

        # Select key classes
        key_classes = [c for c in self.analyzer.classes.values() 
                      if c.is_entity or (c.is_service and len(c.methods) > 3)][:5]

        diagram_lines = ["graph TD"]

        for java_class in key_classes:
            safe_name = java_class.name.replace("-", "_")
            type_emoji = "🔹" if java_class.is_entity else "⚙️"
            
            fields_str = "\\n".join(java_class.fields[:3]) if java_class.fields else ""
            methods_str = "\\n".join(java_class.methods[:3]) if java_class.methods else ""
            
            class_def = f'  {safe_name}["<b>{type_emoji} {java_class.name}</b>\\n---\\n{fields_str}\\n---\\n{methods_str}"]'
            diagram_lines.append(class_def)

        diagram = "\n".join(diagram_lines)
        self.add_mermaid_diagram(diagram, "Key Classes")

    def generate_entity_diagram(self) -> None:
        """Generate entity relationship diagram."""
        self.add_heading("Entity Relationship Overview", 2)

        entities = [c for c in self.analyzer.classes.values() if c.is_entity]

        if not entities:
            self.add_paragraph("*No entities found in this project.*")
            return

        diagram_lines = ["graph TD"]

        for entity in entities[:5]:  # Limit to top 5
            safe_name = entity.name.replace("-", "_")
            fields_str = " | ".join(entity.fields[:3]) if entity.fields else "..."
            diagram_lines.append(f'  {safe_name}["📋 {entity.name}\\n{fields_str}"]')

        diagram = "\n".join(diagram_lines)
        self.add_mermaid_diagram(diagram, "Entity Overview")

    def generate_tech_stack_section(self) -> None:
        """Generate technology stack section."""
        self.add_heading("Technology Stack", 2)

        if self.analyzer.tech_stack:
            tech_list = "- " + "\n- ".join(sorted(self.analyzer.tech_stack))
            self.add_paragraph(tech_list)
        else:
            self.add_paragraph("*Technology stack could not be fully determined.*")

    def generate_package_structure(self) -> None:
        """Generate package structure section."""
        self.add_heading("Package Structure", 2)

        # Group classes by package
        packages: Dict[str, List[JavaClass]] = {}
        for java_class in self.analyzer.classes.values():
            if java_class.package not in packages:
                packages[java_class.package] = []
            packages[java_class.package].append(java_class)

        for package_name in sorted(packages.keys()):
            classes = packages[package_name]
            self.add_heading(f"`{package_name}`", 3)
            
            class_list = []
            for java_class in sorted(classes, key=lambda c: c.name):
                type_label = java_class.type_label
                class_list.append(f"- **{java_class.name}** ({type_label})")
            
            self.doc_lines.append("\n".join(class_list) + "\n")

    def generate_key_components(self) -> None:
        """Generate detailed key components section."""
        self.add_heading("Key Components", 2)

        # Controllers
        controllers = [c for c in self.analyzer.classes.values() if c.is_controller]
        if controllers:
            self.add_heading("REST Controllers", 3)
            for controller in controllers:
                self.add_heading(controller.name, 4)
                self.add_paragraph(f"**Package**: `{controller.package}`")
                self.add_paragraph(f"**File**: `{controller.path}`")
                
                if controller.annotations:
                    annotations = ", ".join(controller.annotations[:5])
                    self.add_paragraph(f"**Annotations**: {annotations}")
                
                if controller.methods:
                    self.add_paragraph("**Methods**:")
                    methods_str = "- " + "\n- ".join(controller.methods[:5])
                    self.doc_lines.append(methods_str + "\n")

        # Services
        services = [c for c in self.analyzer.classes.values() if c.is_service]
        if services:
            self.add_heading("Business Services", 3)
            for service in services:
                self.add_heading(service.name, 4)
                self.add_paragraph(f"**Package**: `{service.package}`")
                self.add_paragraph(f"**File**: `{service.path}`")
                
                if service.methods:
                    self.add_paragraph("**Key Methods**:")
                    methods_str = "- " + "\n- ".join(service.methods[:5])
                    self.doc_lines.append(methods_str + "\n")

        # Repositories
        repositories = [c for c in self.analyzer.classes.values() if c.is_repository]
        if repositories:
            self.add_heading("Data Repositories", 3)
            for repo in repositories:
                self.add_heading(repo.name, 4)
                self.add_paragraph(f"**Package**: `{repo.package}`")
                self.add_paragraph(f"**File**: `{repo.path}`")

    def generate_design_patterns(self) -> None:
        """Generate design patterns identification."""
        self.add_heading("Design Patterns Identified", 2)

        patterns = []

        # Check for MVC
        has_controllers = any(c.is_controller for c in self.analyzer.classes.values())
        has_services = any(c.is_service for c in self.analyzer.classes.values())
        has_entities = any(c.is_entity for c in self.analyzer.classes.values())

        if has_controllers and has_services and has_entities:
            patterns.append("**MVC/Layered Architecture**: Clear separation of presentation, business, and data layers")

        # Check for DTO pattern
        has_dtos = any(c.is_dto for c in self.analyzer.classes.values())
        if has_dtos and has_entities:
            patterns.append("**Data Transfer Object (DTO) Pattern**: Entities are transformed to DTOs for API responses")

        # Check for Repository pattern
        if any(c.is_repository for c in self.analyzer.classes.values()):
            patterns.append("**Repository Pattern**: Data access logic is abstracted behind repository interfaces")

        # Check for Service/Facade pattern
        if has_services:
            patterns.append("**Service/Facade Pattern**: Business logic is centralized in service classes")

        if patterns:
            for pattern in patterns:
                self.doc_lines.append(f"- {pattern}\n")
        else:
            self.add_paragraph("*Common design patterns could not be clearly identified.*")

    def generate_best_practices(self) -> None:
        """Generate best practices section."""
        self.add_heading("Best Practices & Observations", 2)

        observations = []

        # Check for Java version
        if "Java 17" in self.analyzer.tech_stack or "Java 21" in self.analyzer.tech_stack:
            observations.append("✅ Modern Java version (17+) with latest features and improvements")

        # Check for Spring Boot
        if "Spring Boot" in " ".join(self.analyzer.tech_stack):
            observations.append("✅ Uses Spring Boot framework for rapid development and convention-over-configuration")

        # Check for JPA/Hibernate
        if "Spring Data JPA" in self.analyzer.tech_stack:
            observations.append("✅ Uses Spring Data JPA for ORM and database abstraction")

        # Check for validation
        annotations_all = " ".join([ann for c in self.analyzer.classes.values() for ann in c.annotations])
        if "Valid" in annotations_all or "Validated" in annotations_all:
            observations.append("✅ Input validation using annotations")

        # Check for exception handling
        has_exception_handler = any(c.is_exception or "Exception" in c.name 
                                   for c in self.analyzer.classes.values())
        if has_exception_handler:
            observations.append("✅ Custom exception handling for domain-specific errors")

        # Check for Swagger
        if "Swagger" in " ".join(self.analyzer.tech_stack):
            observations.append("✅ API documentation with Swagger/OpenAPI")

        # Check for Lombok
        if "Lombok" in self.analyzer.tech_stack:
            observations.append("✅ Uses Lombok to reduce boilerplate code")

        if observations:
            for obs in observations:
                self.doc_lines.append(f"{obs}\n")

    def generate_recommendations(self) -> None:
        """Generate recommendations section."""
        self.add_heading("Recommendations", 2)

        recommendations = [
            "- 📌 **Add comprehensive unit tests** with JUnit 5 and Mockito for all service layer methods",
            "- 📌 **Implement logging** using SLF4J with appropriate log levels for debugging and monitoring",
            "- 📌 **Add API versioning** to handle backward compatibility in future releases",
            "- 📌 **Document API endpoints** thoroughly with clear examples and use cases",
            "- 📌 **Implement caching strategies** where applicable to improve performance",
            "- 📌 **Add security features** like authentication (JWT) and authorization (Spring Security)",
            "- 📌 **Implement pagination** for list endpoints to handle large datasets efficiently",
            "- 📌 **Add input validation** and error handling middleware for consistent error responses",
        ]

        for rec in recommendations:
            self.doc_lines.append(f"{rec}\n")

    def generate_document(self) -> str:
        """Generate complete documentation."""
        # Title
        self.add_heading(f"{self.analyzer.project_name} - Technical Documentation")
        
        # Introduction
        self.add_paragraph("This document provides a comprehensive technical analysis and architecture documentation for the project.")
        
        # Table of contents
        self.add_heading("Table of Contents", 2)
        self.doc_lines.append("""
1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Package Structure](#package-structure)
4. [Key Components](#key-components)
5. [Design Patterns](#design-patterns)
6. [Best Practices](#best-practices)
7. [Recommendations](#recommendations)

---
""")

        # Generate sections
        self.generate_architecture_overview()
        self.doc_lines.append("\n")
        
        self.generate_data_flow_diagram()
        self.doc_lines.append("\n")
        
        self.generate_component_diagram()
        self.doc_lines.append("\n")
        
        self.generate_tech_stack_section()
        self.doc_lines.append("\n")
        
        self.generate_package_structure()
        self.doc_lines.append("\n")
        
        self.generate_entity_diagram()
        self.doc_lines.append("\n")
        
        self.generate_class_diagram()
        self.doc_lines.append("\n")
        
        self.generate_key_components()
        self.doc_lines.append("\n")
        
        self.generate_design_patterns()
        self.doc_lines.append("\n")
        
        self.generate_best_practices()
        self.doc_lines.append("\n")
        
        self.generate_recommendations()

        return "\n".join(self.doc_lines)


def generate_documentation_for_repos(temp_root: Path, output_root: Path) -> None:
    """Generate documentation for all repositories in temp folder."""
    
    # Create output directory
    output_root.mkdir(parents=True, exist_ok=True)
    
    # Find repositories
    if not temp_root.exists():
        print(f"Temp folder not found: {temp_root}")
        return
    
    repos = [d for d in temp_root.iterdir() if d.is_dir() and (d / ".git").exists()]
    
    if not repos:
        print(f"No repositories found in {temp_root}")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for repo_path in repos:
        print(f"\nAnalyzing repository: {repo_path.name}")
        
        # Analyze repository
        analyzer = JavaCodeAnalyzer(repo_path)
        analyzer.analyze()
        
        print(f"  Found {len(analyzer.classes)} Java classes")
        print(f"  Tech stack: {', '.join(analyzer.tech_stack)}")
        
        # Generate documentation
        doc_gen = DocumentationGenerator(analyzer)
        documentation = doc_gen.generate_document()
        
        # Save documentation
        output_file = output_root / f"{repo_path.name}_{timestamp}.md"
        output_file.write_text(documentation, encoding='utf-8')
        
        print(f"  ✅ Documentation saved to: {output_file.relative_to(Path.cwd())}")


def main() -> None:
    """Main entry point."""
    # Get workspace root (script is in .github/tools)
    script_dir = Path(__file__).resolve().parent
    workspace_root = script_dir.parent.parent
    
    temp_root = workspace_root / "temp"
    output_root = workspace_root / "docs_report"
    
    print("=" * 70)
    print("Java Repository Documentation Generator")
    print("=" * 70)
    print(f"Workspace: {workspace_root}")
    print(f"Repository folder: {temp_root}")
    print(f"Output folder: {output_root}")
    print("=" * 70)
    
    generate_documentation_for_repos(temp_root, output_root)
    
    print("\n" + "=" * 70)
    print("Documentation generation completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
