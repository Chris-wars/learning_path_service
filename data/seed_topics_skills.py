import os
import random
import time
import requests
import json  # Importiere das JSON-Modul für verbesserte Fehlerausgabe

# -----------------------------
# Configuration
# -----------------------------
TOPICS_API_BASE = os.getenv("TOPICS_API_BASE", "http://localhost:5000").rstrip("/")
PARENT_TOPICS = [
    ("Web Development Fundamentals", "Core concepts: HTML, CSS, JS."),
    ("Python Programming", "Python syntax, data structures, OOP, tooling."),
    ("Data Science & Analytics", "Data wrangling, visualization, statistics."),
    ("Databases & SQL", "Relational modeling, SQL queries, optimization."),
    ("DevOps & CI/CD", "Automation, pipelines, containers, IaC."),
    ("Cloud Computing", "AWS, Azure, GCP basics and best practices."),
    ("Cybersecurity", "Security fundamentals, OWASP, secure coding."),
    ("Mobile Development", "Android, iOS, cross-platform basics."),
    ("Software Testing & QA", "Unit, integration, E2E, test strategy."),
    ("AI & Machine Learning", "ML basics, model training, deployment."),
]

# Subtopics per parent (feel free to tweak or add more):
SUBTOPICS = {
    "Web Development Fundamentals": [
        "HTML & Semantic Structure", "CSS Basics", "Modern JavaScript (ES6+)",
        "Responsive Design", "Accessibility (a11y)", "Frontend Tooling"
    ],
    "Python Programming": [
        "Python Syntax & Control Flow", "Data Structures", "OOP in Python",
        "Virtual Envs & Packaging", "Typing & Pydantic", "Flask & FastAPI Basics"
    ],
    "Data Science & Analytics": [
        "Pandas for Data Wrangling", "Data Visualization", "Statistics Fundamentals",
        "Jupyter & Notebooks", "Feature Engineering"
    ],
    "Databases & SQL": [
        "Relational Modeling", "SQL CRUD & Joins", "Indexes & Query Plans",
        "Transactions & Isolation", "ORMs (SQLAlchemy)"
    ],
    "DevOps & CI/CD": [
        "Git & Branching", "CI Pipelines", "Docker Basics",
        "Kubernetes Basics", "Infrastructure as Code"
    ],
    "Cloud Computing": [
        "AWS Foundations", "Azure Foundations", "GCP Foundations",
        "Cloud Networking Basics", "Serverless Basics"
    ],
    "Cybersecurity": [
        "Security Fundamentals", "OWASP Top 10", "Secure Coding Practices",
        "Identity & Access Management", "Network Security"
    ],
    "Mobile Development": [
        "Android Basics (Kotlin)", "iOS Basics (Swift)", "Cross-platform (Flutter)",
        "Mobile UI/UX Basics", "Local Storage & APIs"
    ],
    "Software Testing & QA": [
        "Unit Testing", "Integration Testing", "End-to-End Testing",
        "Test Automation", "Performance Testing"
    ],
    "AI & Machine Learning": [
        "ML Fundamentals", "Supervised Learning", "Model Evaluation",
        "Intro to Deep Learning", "ML Ops Basics"
    ],
}

# Skills templates per subtopic (we’ll pick 2–4 randomly)
SKILLS_TEMPLATES = {
    "HTML & Semantic Structure": [
        "HTML Structure", "Semantic Tags", "Forms & Validation", "SEO Basics"
    ],
    "CSS Basics": [
        "Box Model", "Flexbox", "Grid Layout", "Selectors & Specificity"
    ],
    "Modern JavaScript (ES6+)": [
        "Arrow Functions", "Promises & Async/Await", "Modules", "DOM Manipulation"
    ],
    "Responsive Design": [
        "Media Queries", "Fluid Layouts", "Mobile-first Design"
    ],
    "Accessibility (a11y)": [
        "ARIA Basics", "Keyboard Navigation", "Color Contrast"
    ],
    "Frontend Tooling": [
        "NPM & Scripts", "Bundlers (Vite/Webpack)", "Linters/Formatters"
    ],

    "Python Syntax & Control Flow": [
        "Variables & Types", "Control Flow", "Functions", "Error Handling"
    ],
    "Data Structures": [
        "Lists & Tuples", "Dictionaries & Sets", "List Comprehensions"
    ],
    "OOP in Python": [
        "Classes & Objects", "Inheritance", "Dataclasses"
    ],
    "Virtual Envs & Packaging": [
        "venv Basics", "pip & requirements", "Packaging a Module"
    ],
    "Typing & Pydantic": [
        "Type Hints", "Pydantic Models", "Validation"
    ],
    "Flask & FastAPI Basics": [
        "Routing", "Request/Response Models", "Middleware Basics"
    ],

    "Pandas for Data Wrangling": [
        "DataFrames", "Filtering & Aggregation", "Merging & Joins"
    ],
    "Data Visualization": [
        "Matplotlib Basics", "Plotly Basics", "Seaborn Basics"
    ],
    "Statistics Fundamentals": [
        "Descriptive Stats", "Probability Basics", "Hypothesis Testing"
    ],
    "Jupyter & Notebooks": [
        "Cells & Magics", "Markdown & Visuals", "Reproducibility"
    ],
    "Feature Engineering": [
        "Scaling & Encoding", "Feature Selection", "Handling Missing Values"
    ],

    "Relational Modeling": [
        "Entities & Relationships", "Normalization", "Schema Design"
    ],
    "SQL CRUD & Joins": [
        "SELECT & Filtering", "INNER/LEFT JOINs", "Aggregations"
    ],
    "Indexes & Query Plans": [
        "B-Tree Indexes", "EXPLAIN/ANALYZE", "Performance Tuning"
    ],
    "Transactions & Isolation": [
        "ACID", "Isolation Levels", "Locking"
    ],
    "ORMs (SQLAlchemy)": [
        "Models & Migrations", "Relationships", "Query Patterns"
    ],

    "Git & Branching": [
        "Git Basics", "Branching Models", "Pull Requests"
    ],
    "CI Pipelines": [
        "Pipeline Basics", "Test & Lint Stages", "Artifacts"
    ],
    "Docker Basics": [
        "Dockerfile", "Images & Containers", "Volumes & Networks"
    ],
    "Kubernetes Basics": [
        "Pods & Deployments", "Services & Ingress", "ConfigMaps/Secrets"
    ],
    "Infrastructure as Code": [
        "Terraform Basics", "State & Modules", "Plan/Apply"
    ],

    "AWS Foundations": [
        "IAM Basics", "EC2 & S3", "VPC Basics"
    ],
    "Azure Foundations": [
        "Azure AD", "VMs & Storage", "VNets Basics"
    ],
    "GCP Foundations": [
        "IAM & Projects", "Compute & Storage", "VPC Basics"
    ],
    "Cloud Networking Basics": [
        "CIDR & Subnets", "Routing & Gateways", "Security Groups"
    ],
    "Serverless Basics": [
        "Functions-as-a-Service", "Event Triggers", "Cold Starts"
    ],

    "Security Fundamentals": [
        "CIA Triad", "Security Policies", "Threat Modeling"
    ],
    "OWASP Top 10": [
        "Injection", "Auth & Session", "Sensitive Data Exposure"
    ],
    "Secure Coding Practices": [
        "Input Validation", "Output Encoding", "Secrets Management"
    ],
    "Identity & Access Management": [
        "AuthN vs AuthZ", "OAuth2/OIDC", "RBAC"
    ],
    "Network Security": [
        "Firewalls", "TLS/HTTPS", "VPNs"
    ],

    "Android Basics (Kotlin)": [
        "Activities & Fragments", "Layouts", "Networking"
    ],
    "iOS Basics (Swift)": [
        "ViewControllers", "Auto Layout", "URLSession"
    ],
    "Cross-platform (Flutter)": [
        "Widgets", "State Management", "HTTP & JSON"
    ],
    "Mobile UI/UX Basics": [
        "Navigation Patterns", "Touch Targets", "Notifications"
    ],
    "Local Storage & APIs": [
        "SQLite/Room/CoreData", "REST APIs", "Auth Tokens"
    ],

    "Unit Testing": [
        "Test Structure", "Assertions", "Fixtures/Mocks"
    ],
    "Integration Testing": [
        "Service Wiring", "Test Data", "Test Environments"
    ],
    "End-to-End Testing": [
        "Browser Automation", "API E2E", "Test Reports"
    ],
    "Test Automation": [
        "CI Integration", "Parallel Runs", "Flaky Tests"
    ],
    "Performance Testing": [
        "Load vs Stress", "Metrics & SLAs", "Bottlenecks"
    ],

    "ML Fundamentals": [
        "Train/Val/Test Split", "Bias/Variance", "Overfitting"
    ],
    "Supervised Learning": [
        "Regression", "Classification", "Model Selection"
    ],
    "Model Evaluation": [
        "Accuracy/Precision/Recall", "ROC-AUC", "Cross-Validation"
    ],
    "Intro to Deep Learning": [
        "Neural Nets Basics", "Activation Functions", "Optimizers"
    ],
    "ML Ops Basics": [
        "Model Packaging", "Serving", "Monitoring"
    ],
}

DIFFICULTY = ["beginner", "intermediate", "advanced"]


def post_json(url, payload):
    """
    Sendet eine POST-Anfrage und verarbeitet Fehler, um detaillierte Informationen
    über HTTP-Fehlercodes bereitzustellen.
    """
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        print(f"\n[ERROR] HTTPError: {e}")
        print(f"URL: {e.response.url}")
        print(f"Status Code: {e.response.status_code}")
        print(f"Response Body: {e.response.text}")
        print(f"Payload sent: {json.dumps(payload, indent=2)}")
        raise e  # Den Fehler erneut werfen, damit der Traceback sichtbar ist


def seed():
    """
    Seeds the topics and skills into the database via the API.
    """
    print(f"Using Topics API at: {TOPICS_API_BASE}")

    # 1) Create parent topics
    parent_id_map = {}
    for name, desc in PARENT_TOPICS:
        t = post_json(f"{TOPICS_API_BASE}/topics", {
            "name": name,
            "description": desc
        })
        parent_id_map[name] = t["id"]
        print("Created parent topic:", name)

    # 2) Create subtopics (children) under each parent
    subtopic_ids = {}  # name -> id
    total_topics = 0
    for parent_name, sub_list in SUBTOPICS.items():
        if parent_name not in parent_id_map:
            print(f"[WARN] Parent topic '{parent_name}' not found. Skipping its subtopics.")
            continue
            
        for sub_name in sub_list:
            t = post_json(f"{TOPICS_API_BASE}/topics", {
                "name": sub_name,
                "description": f"{sub_name} under {parent_name}",
                "parentTopicID": parent_id_map[parent_name]  # Korrigierter Feldname
            })
            subtopic_ids[sub_name] = t["id"]
            total_topics += 1
            print(f"  Created subtopic: {sub_name}")

    print(f"Total topics (parents + subtopics): {len(PARENT_TOPICS) + total_topics}")

    # 3) Create skills per subtopic (2–4 each)
    total_skills = 0
    # Iteriere über die Subtopics, die wir erfolgreich erstellt haben
    for sub_name, sub_id in subtopic_ids.items():
        if sub_name not in SKILLS_TEMPLATES:
            # Das ist in unseren Daten nicht der Fall, aber es macht das Skript robuster
            print(f"[WARN] No skill templates for subtopic '{sub_name}'. Skipping.")
            continue
            
        skill_names = SKILLS_TEMPLATES[sub_name]
        k = random.randint(2, min(4, len(skill_names)))
        chosen = random.sample(skill_names, k)
        
        for sn in chosen:
            payload = {
                "name": sn,
                "topicID": sub_id,  # Richtig: "topicID"
                "difficulty": random.choice(DIFFICULTY)
            }
            s = post_json(f"{TOPICS_API_BASE}/skills", payload)
            total_skills += 1
            print(f"    Created skill: {sn} (topic: {sub_name})")
            time.sleep(0.02)  # tiny delay to be kind

    print(f"Total skills created: {total_skills}")


if __name__ == "__main__":
    seed()