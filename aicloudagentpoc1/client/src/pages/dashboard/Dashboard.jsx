// pages/dashboard/Dashboard.jsx
import ProjectsList from "./ProjectsList";

export default function Dashboard() {
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Your Projects</h1>
        <p className="dashboard-subtitle">
          Manage, deploy, and evolve your cloud infrastructure with AI
        </p>
      </header>

      <section className="dashboard-content">
        <ProjectsList />
      </section>
    </div>
  );
}
