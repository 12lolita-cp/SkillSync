
import { useState } from 'react';
import './App.css';

const navigation = [
  { name: 'Overview', icon: 'home' },
  { name: 'My Profile', icon: 'user' },
  { name: 'My Skills', icon: 'sparkles' },
  { name: 'My Projects', icon: 'folder' },
  { name: 'Internships', icon: 'briefcase' },
  { name: 'Applications', icon: 'send' }
];

function Icon({ name, size = 19 }) {
  const paths = {
    home: <><path d="m3 10 9-7 9 7" /><path d="M5 9v11h14V9" /><path d="M9 20v-6h6v6" /></>,
    user: <><circle cx="12" cy="8" r="4" /><path d="M4 21a8 8 0 0 1 16 0" /></>,
    sparkles: <><path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3Z" /><path d="m19 14 1 2.5 2.5 1-2.5 1L19 21l-1-2.5-2.5-1 2.5-1 1-2.5Z" /></>,
    folder: <><path d="M3 6a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6Z" /></>,
    briefcase: <><rect x="3" y="7" width="18" height="14" rx="2" /><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18M10 12v2h4v-2" /></>,
    send: <><path d="m22 2-7 20-4-9-9-4 20-7Z" /><path d="M22 2 11 13" /></>,
    plus: <><path d="M12 5v14M5 12h14" /></>,
    arrow: <><path d="M7 17 17 7M7 7h10v10" /></>,
    check: <path d="m5 12 4 4L19 6" />,
    menu: <><path d="M4 6h16M4 12h16M4 18h16" /></>,
    close: <><path d="m18 6-12 12M6 6l12 12" /></>,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    userCircle: <><circle cx="12" cy="12" r="9" /><circle cx="12" cy="9" r="3" /><path d="M6.5 19a6 6 0 0 1 11 0" /></>
  };

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {paths[name]}
    </svg>
  );
}

function EmptyState({ icon, title, description, action, onAction }) {
  return (
    <div className="empty-state">
      <div className="empty-icon"><Icon name={icon} size={25} /></div>
      <h3>{title}</h3>
      <p>{description}</p>
      {action && (
        <button className="text-action" onClick={onAction}>
          {action} <span>↗</span>
        </button>
      )}
    </div>
  );
}

function App() {
  const [activePage, setActivePage] = useState('Overview');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const [profile, setProfile] = useState({
    name: '',
    email: '',
    college: '',
    branch: '',
    year: ''
  });

  const [skills, setSkills] = useState([]);
  const [projects, setProjects] = useState([]);
  const [internships] = useState([]);
  const [applications] = useState([]);

  const [skillName, setSkillName] = useState('');
  const [skillLevel, setSkillLevel] = useState('Beginner');

  const [projectName, setProjectName] = useState('');
  const [projectDescription, setProjectDescription] = useState('');

  const [profileSaved, setProfileSaved] = useState(false);
  const [notice, setNotice] = useState('');

  const completedFields = Object.values(profile).filter(
    (value) => value.trim() !== ''
  ).length;

  const profileProgress = Math.round((completedFields / 5) * 100);

  const goTo = (page) => {
    setActivePage(page);
    setMobileMenuOpen(false);
    setNotice('');
  };

  const addSkill = (event) => {
    event.preventDefault();

    if (!skillName.trim()) return;

    setSkills([
      ...skills,
      { id: Date.now(), name: skillName.trim(), level: skillLevel }
    ]);

    setSkillName('');
    setSkillLevel('Beginner');
    setNotice('Skill added successfully!');
  };

  const removeSkill = (id) => {
    setSkills(skills.filter((skill) => skill.id !== id));
  };

  const addProject = (event) => {
    event.preventDefault();

    if (!projectName.trim()) return;

    setProjects([
      ...projects,
      {
        id: Date.now(),
        name: projectName.trim(),
        description: projectDescription.trim()
      }
    ]);

    setProjectName('');
    setProjectDescription('');
    setNotice('Project added successfully!');
  };

  const saveProfile = (event) => {
    event.preventDefault();
    setProfileSaved(true);
    setNotice('Profile saved for this session!');
  };

  const renderOverview = () => (
    <>
      <section className="welcome-section">
        <div>
          <span className="eyebrow">YOUR STUDENT WORKSPACE</span>
          <h1>
            {profile.name.trim()
              ? `Hello, ${profile.name.trim().split(' ')[0]}.`
              : 'Make your next move.'}
          </h1>
          <p>
            Your skills, projects and opportunities — all in one place.
          </p>
        </div>

        <div className="welcome-decoration" aria-hidden="true">
          <span className="decoration-circle circle-one" />
          <span className="decoration-circle circle-two" />
          <span className="decoration-circle circle-three" />
        </div>
      </section>

      <section className="stats-grid">
        <div className="stat-card sage-card">
          <div className="stat-top">
            <span>My skills</span>
            <Icon name="sparkles" />
          </div>
          <strong>{skills.length}</strong>
          <span className="stat-note">Skills in your profile</span>
        </div>

        <div className="stat-card peach-card">
          <div className="stat-top">
            <span>My projects</span>
            <Icon name="folder" />
          </div>
          <strong>{projects.length}</strong>
          <span className="stat-note">Projects showcased</span>
        </div>

        <div className="stat-card beige-card">
          <div className="stat-top">
            <span>Internships</span>
            <Icon name="briefcase" />
          </div>
          <strong>{internships.length}</strong>
          <span className="stat-note">Available opportunities</span>
        </div>

        <div className="stat-card cream-card">
          <div className="stat-top">
            <span>Applications</span>
            <Icon name="send" />
          </div>
          <strong>{applications.length}</strong>
          <span className="stat-note">Applications submitted</span>
        </div>
      </section>

      <section className="bento-grid">
        <div className="panel profile-progress-panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">GETTING STARTED</span>
              <h2>Your profile</h2>
            </div>
            <div className="round-icon"><Icon name="userCircle" /></div>
          </div>

          <div className="progress-number">
            <strong>{profileProgress}%</strong>
            <span>completed</span>
          </div>

          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${profileProgress}%` }}
            />
          </div>

          <p className="muted">
            Add your details to help others get to know you.
          </p>

          <button className="outline-btn" onClick={() => goTo('My Profile')}>
            Complete profile <Icon name="arrow" size={15} />
          </button>
        </div>

        <div className="panel quick-actions-panel">
          <span className="eyebrow">MAKE SOMETHING HAPPEN</span>
          <h2>Quick actions</h2>
          <p className="muted">A few small steps to build your portfolio.</p>

          <button className="quick-action" onClick={() => goTo('My Skills')}>
            <span className="action-icon sage-action"><Icon name="sparkles" /></span>
            <span><strong>Add a skill</strong><small>Show what you know</small></span>
            <Icon name="arrow" size={16} />
          </button>

          <button className="quick-action" onClick={() => goTo('My Projects')}>
            <span className="action-icon peach-action"><Icon name="folder" /></span>
            <span><strong>Add a project</strong><small>Show what you've built</small></span>
            <Icon name="arrow" size={16} />
          </button>
        </div>

        <div className="panel skills-preview-panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">YOUR TOOLKIT</span>
              <h2>Skills</h2>
            </div>
            <button className="text-action" onClick={() => goTo('My Skills')}>
              View all <span>↗</span>
            </button>
          </div>

          {skills.length === 0 ? (
            <EmptyState
              icon="sparkles"
              title="Your skills live here"
              description="Add your first skill and start building your toolkit."
              action="Add a skill"
              onAction={() => goTo('My Skills')}
            />
          ) : (
            <div className="preview-tags">
              {skills.slice(0, 6).map((skill) => (
                <span className="skill-tag" key={skill.id}>{skill.name}</span>
              ))}
            </div>
          )}
        </div>

        <div className="panel projects-preview-panel">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">YOUR WORK</span>
              <h2>Recent projects</h2>
            </div>
            <button className="text-action" onClick={() => goTo('My Projects')}>
              View all <span>↗</span>
            </button>
          </div>

          {projects.length === 0 ? (
            <EmptyState
              icon="folder"
              title="Nothing here just yet"
              description="Your projects will appear here when you add them."
              action="Add a project"
              onAction={() => goTo('My Projects')}
            />
          ) : (
            <div className="project-preview-list">
              {projects.slice(0, 3).map((project) => (
                <div className="project-preview" key={project.id}>
                  <span className="project-dot" />
                  <div>
                    <strong>{project.name}</strong>
                    <p>{project.description || 'No description added.'}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </>
  );

  const renderProfile = () => (
    <div className="page-narrow">
      <div className="page-intro">
        <span className="eyebrow">ABOUT YOU</span>
        <h1>My profile</h1>
        <p>Make it easy for people to know who you are.</p>
      </div>

      <div className="panel form-panel">
        <form onSubmit={saveProfile}>
          <div className="form-grid">
            <div className="form-group">
              <label>Full name</label>
              <input
                value={profile.name}
                placeholder="Your full name"
                onChange={(e) => {
                  setProfile({ ...profile, name: e.target.value });
                  setProfileSaved(false);
                }}
              />
            </div>

            <div className="form-group">
              <label>Email address</label>
              <input
                type="email"
                value={profile.email}
                placeholder="you@example.com"
                onChange={(e) => {
                  setProfile({ ...profile, email: e.target.value });
                  setProfileSaved(false);
                }}
              />
            </div>

            <div className="form-group">
              <label>College</label>
              <input
                value={profile.college}
                placeholder="Your college name"
                onChange={(e) => {
                  setProfile({ ...profile, college: e.target.value });
                  setProfileSaved(false);
                }}
              />
            </div>

            <div className="form-group">
              <label>Branch / Department</label>
              <input
                value={profile.branch}
                placeholder="e.g. Computer Science"
                onChange={(e) => {
                  setProfile({ ...profile, branch: e.target.value });
                  setProfileSaved(false);
                }}
              />
            </div>

            <div className="form-group">
              <label>Year of study</label>
              <select
                value={profile.year}
                onChange={(e) => {
                  setProfile({ ...profile, year: e.target.value });
                  setProfileSaved(false);
                }}
              >
                <option value="">Select your year</option>
                <option value="1st Year">1st Year</option>
                <option value="2nd Year">2nd Year</option>
                <option value="3rd Year">3rd Year</option>
                <option value="4th Year">4th Year</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <button className="primary-btn" type="submit">
            Save profile
          </button>
          {profileSaved && <span className="success-message">Saved for this session ✓</span>}
        </form>
      </div>
    </div>
  );

  const renderSkills = () => (
    <div className="page-narrow">
      <div className="page-intro">
        <span className="eyebrow">WHAT YOU KNOW</span>
        <h1>My skills</h1>
        <p>Collect the skills that make you, you.</p>
      </div>

      <div className="panel form-panel">
        <h2>Add a skill</h2>
        <form onSubmit={addSkill}>
          <div className="form-grid">
            <div className="form-group">
              <label>Skill name</label>
              <input
                value={skillName}
                placeholder="e.g. Python, UI Design"
                onChange={(e) => setSkillName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Proficiency</label>
              <select
                value={skillLevel}
                onChange={(e) => setSkillLevel(e.target.value)}
              >
                <option>Beginner</option>
                <option>Intermediate</option>
                <option>Advanced</option>
              </select>
            </div>
          </div>
          <button className="primary-btn" type="submit">
            <Icon name="plus" size={16} /> Add skill
          </button>
        </form>
      </div>

      <div className="panel list-panel">
        <div className="panel-heading">
          <h2>Your toolkit</h2>
          <span className="count-label">{skills.length} skills</span>
        </div>

        {skills.length === 0 ? (
          <EmptyState
            icon="sparkles"
            title="Your toolkit is waiting"
            description="Skills you add will show up here."
          />
        ) : (
          <div className="item-list">
            {skills.map((skill) => (
              <div className="list-item" key={skill.id}>
                <div>
                  <strong>{skill.name}</strong>
                  <span className="level-label">{skill.level}</span>
                </div>
                <button className="remove-btn" onClick={() => removeSkill(skill.id)}>
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  const renderProjects = () => (
    <div className="page-narrow">
      <div className="page-intro">
        <span className="eyebrow">WHAT YOU'VE BUILT</span>
        <h1>My projects</h1>
        <p>Every project tells a little story about what you can do.</p>
      </div>

      <div className="panel form-panel">
        <h2>Add a project</h2>
        <form onSubmit={addProject}>
          <div className="form-group">
            <label>Project name</label>
            <input
              value={projectName}
              placeholder="Give your project a name"
              onChange={(e) => setProjectName(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={projectDescription}
              placeholder="What does it do? What did you learn?"
              rows="4"
              onChange={(e) => setProjectDescription(e.target.value)}
            />
          </div>

          <button className="primary-btn" type="submit">
            <Icon name="plus" size={16} /> Add project
          </button>
        </form>
      </div>

      <div className="panel list-panel">
        <div className="panel-heading">
          <h2>Your projects</h2>
          <span className="count-label">{projects.length} projects</span>
        </div>

        {projects.length === 0 ? (
          <EmptyState
            icon="folder"
            title="Your portfolio starts here"
            description="Add a project to give your work a place to shine."
          />
        ) : (
          <div className="project-cards">
            {projects.map((project) => (
              <article className="project-card" key={project.id}>
                <div className="project-card-icon"><Icon name="folder" /></div>
                <h3>{project.name}</h3>
                <p>{project.description || 'No description added.'}</p>
              </article>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  const renderInternships = () => (
    <div className="page-narrow">
      <div className="page-intro">
        <span className="eyebrow">YOUR NEXT OPPORTUNITY</span>
        <h1>Internships</h1>
        <p>Discover opportunities to learn, build and grow.</p>
      </div>
      <div className="panel list-panel">
        <EmptyState
          icon="briefcase"
          title="No opportunities yet"
          description="Internship listings will appear here when they are added to SkillSync."
        />
      </div>
    </div>
  );

  const renderApplications = () => (
    <div className="page-narrow">
      <div className="page-intro">
        <span className="eyebrow">KEEP TRACK</span>
        <h1>Applications</h1>
        <p>All your internship applications, in one place.</p>
      </div>
      <div className="panel list-panel">
        <EmptyState
          icon="send"
          title="Your application journey starts here"
          description="When you apply for an internship, its status will show up here."
        />
      </div>
    </div>
  );

  const pageContent = () => {
    switch (activePage) {
      case 'Overview': return renderOverview();
      case 'My Profile': return renderProfile();
      case 'My Skills': return renderSkills();
      case 'My Projects': return renderProjects();
      case 'Internships': return renderInternships();
      case 'Applications': return renderApplications();
      default: return renderOverview();
    }
  };

  return (
    <div className="app-shell">
      {mobileMenuOpen && (
        <button
          className="mobile-overlay"
          aria-label="Close navigation"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      <aside className={`sidebar ${mobileMenuOpen ? 'sidebar-open' : ''}`}>
        <div className="brand">
          <div className="brand-mark">S</div>
          <span>skillsync<span className="brand-dot">.</span></span>
        </div>

        <span className="nav-label">WORKSPACE</span>
        <nav className="nav-list">
          {navigation.map((item) => (
            <button
              key={item.name}
              className={`nav-item ${activePage === item.name ? 'nav-active' : ''}`}
              onClick={() => goTo(item.name)}
            >
              <Icon name={item.icon} />
              <span>{item.name}</span>
              {activePage === item.name && <span className="active-indicator" />}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-note">
            <span className="note-sparkle">✳</span>
            <p>Small steps.<br />Big possibilities.</p>
          </div>
          <span className="sidebar-version">SKILLSYNC · STUDENT EDITION</span>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <button
            className="mobile-menu-btn"
            aria-label="Open navigation"
            onClick={() => setMobileMenuOpen(true)}
          >
            <Icon name="menu" />
          </button>

          <div className="breadcrumb">
            <span>Workspace</span>
            <span className="breadcrumb-divider">/</span>
            <strong>{activePage}</strong>
          </div>

          <button className="top-profile" onClick={() => goTo('My Profile')}>
            <span className="avatar">
              {profile.name.trim() ? profile.name.trim().charAt(0).toUpperCase() : <Icon name="user" size={17} />}
            </span>
            <span>{profile.name.trim() || 'My profile'}</span>
          </button>
        </header>

        <div className="content-area">
          {notice && (
            <div className="notice-message">
              <Icon name="check" size={16} /> {notice}
              <button onClick={() => setNotice('')} aria-label="Dismiss">×</button>
            </div>
          )}
          {pageContent()}
          <footer className="page-footer">
            Made for students, built for possibilities. <span>✳</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
