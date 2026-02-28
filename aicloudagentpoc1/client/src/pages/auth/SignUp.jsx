// pages/auth/SignIn.jsx
export default function SignUp() {
  return (
    <div className="auth-page">
      <div className="auth-container">
        <h2>Sign In</h2>
        <p className="auth-subtitle">
          Access your projects and manage cloud deployments
        </p>

        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />

        <button className="auth-btn">Sign Up</button>
      </div>
    </div>
  );
}
