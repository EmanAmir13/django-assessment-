# django-project

Project and Task Management API with role-based permissions and JWT authentication.

1. Models:

- User: Use Django's default user model or a custom one with fields like email,
  username, and role (Admin, Member).
- Project: Contains title, description, and a foreign key to User (creator).
- Task: Includes title, description, status (To Do, In Progress,
  Completed), and a foreign key to Project.

2. API Endpoints:

- Authentication:
  ■ Register and login using JWT.
- Projects:
  ■ CRUD operations. Only Admins can create or delete projects.
- Tasks:
  ■ CRUD operations. Only Admins can create or delete tasks. Members can
  update task statuses.

3. Permissions:
    - Only project creators (Admins) can manage their projects.
    - Members can view projects and update the status of tasks assigned to them.