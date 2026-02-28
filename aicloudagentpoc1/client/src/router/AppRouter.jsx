// router/AppRouter.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignIn from "../pages/auth/SignIn";
import SignUp from "../pages/auth/SignUp";
import Dashboard from "../pages/dashboard/Dashboard";
import ProjectChat from "../pages/chat/ProjectChat";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/signin" element={<SignIn/>} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/projects/:projectId/chat" element={<ProjectChat />} />
      </Routes>
    </BrowserRouter>
  );
}
