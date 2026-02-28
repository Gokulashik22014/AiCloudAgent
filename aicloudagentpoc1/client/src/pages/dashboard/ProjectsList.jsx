// pages/dashboard/ProjectsList.jsx
import { useNavigate } from "react-router-dom";

export default function ProjectsList() {
  const navigate = useNavigate();

  const projects = [
    { id: "proj-1", name: "AI Infra Bot", updatedAt: "2 hours ago" },
    { id: "proj-2", name: "E-commerce Backend", updatedAt: "1 day ago" },
  ];

  if (projects.length === 0) {
    return (
      <div className="projects-empty">
        <h3>No projects yet</h3>
        <p>Create your first project and deploy your code with AI.</p>
        <button className="primary-btn">Create Project</button>
      </div>
    );
  }

  return (
    <div className="projects-grid">
      {projects.map((project) => (
        <div
          key={project.id}
          className="project-card"
          onClick={() => navigate(`/projects/${project.id}/chat`)}
        >
          <h3>{project.name}</h3>
          <p className="project-meta">
            Last updated · {project.updatedAt}
          </p>
        </div>
      ))}

      <div className="project-card project-card-add">
        <button className="add-project-btn">+ New Project</button>
      </div>
    </div>
  );
}
