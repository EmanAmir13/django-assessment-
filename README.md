# Task Management API

## Overview

This project is a REST API for managing tasks within a system where tasks can be associated with specific projects. It allows users to list, create, update, and delete tasks. The API is built using Django and the Django Rest Framework (DRF). 

### Key Features:
- List all tasks with pagination
- Create tasks (Only Admin users)
- Retrieve, update, or delete tasks (Admins can delete, Members can update task status)
- Supports CRUD operations for tasks
- Role-based permissions for task actions
- Validates task status updates based on user roles

## Table of Contents
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Task List & Create](#task-list-create)
  - [Task Detail](#task-detail)
- [Permissions](#permissions)
- [Task Model](#task-model)
- [Task Serializer](#task-serializer)
- [Pagination](#pagination)
- [Testing](#testing)
- [Contributing](#contributing)

## Installation

Follow these steps to get the project up and running locally.

### Prerequisites

- Python 3.8+
- Django 4.x
- Django Rest Framework
- PostgreSQL (or any other database supported by Django)

### Steps to Install

1. Clone the repository:

   ```bash
   git clone https://github.com/EmanAmir13/django-assessment-.git
   cd django-assessment-
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser for administrative purposes:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. The API will be available at: `http://127.0.0.1:8000/`

## API Endpoints

### Task List & Create (`/api/tasks/`)

#### **GET /api/tasks/**
- Retrieves a list of all tasks with pagination.
- Query parameters: 
  - `page`: For pagination (default: 1)

#### **POST /api/tasks/**
- Creates a new task.
- **Request Body**:
  ```json
  {
    "title": "Task Title",
    "description": "Task Description",
    "status": "to_do",
    "project": 1
  }
  ```
  - `status`: One of the following values: `to_do`, `in_progress`, `completed`
  - `project`: ID of an existing project to associate the task with.
  - **Admin-only**: Only Admin users can create tasks.

#### **Response**:
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Task Title",
    "description": "Task Description",
    "status": "to_do",
    "project": 1,
    "created_at": "2025-02-17T12:00:00Z",
    "updated_at": "2025-02-17T12:00:00Z"
  }
}
```

---

### Task Detail (`/api/tasks/{id}/`)

#### **GET /api/tasks/{id}/**
- Retrieves details of a specific task.

#### **PATCH /api/tasks/{id}/**
- Partially updates a task (typically used to update the task status).
- **Request Body**:
  ```json
  {
    "status": "in_progress"
  }
  ```

#### **PUT /api/tasks/{id}/**
- Fully updates a task.
- **Request Body**:
  ```json
  {
    "title": "Updated Task Title",
    "description": "Updated Description",
    "status": "completed",
    "project": 1
  }
  ```

#### **DELETE /api/tasks/{id}/**
- Deletes a task (Admin-only).

### Permissions

- **Admin Users**: Can create, update, delete tasks, and manage all aspects of the task.
- **Member Users**: Can only update the status of tasks (using `PATCH` or `PUT`).
- **Authenticated Users**: Can retrieve tasks and make requests according to their role.
  
### Task Model

The `Task` model consists of the following fields:
- `id`: Auto-incremented ID for each task (Primary Key).
- `title`: A string field for the task title.
- `description`: A text field for a detailed description of the task.
- `status`: A choice field representing the task's current state. Options include:
  - `to_do`: The task is yet to be started.
  - `in_progress`: The task is currently being worked on.
  - `completed`: The task is finished.
- `project`: A foreign key relation to the `Project` model. A task must be linked to a project.
- `created_at`: The timestamp when the task was created.
- `updated_at`: The timestamp when the task was last updated.

### Task Serializer

The `TaskSerializer` handles validation and serialization of `Task` data. The following fields are validated:
- Only members can update the `status` field of the task. If a member tries to update fields other than `status`, a validation error is raised.

```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### Pagination

The API uses `PageNumberPagination` for task listing, which allows paginated results. The default page size is set to 10, but you can modify it based on your needs.

Example request:
```bash
GET /api/tasks/?page=2
```

The API will return tasks in a paginated format, including metadata for pagination:

```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/tasks/?page=2",
  "previous": "http://127.0.0.1:8000/api/tasks/?page=1",
  "results": [
    {
      "id": 1,
      "title": "Task Title",
      "description": "Task Description",
      "status": "to_do",
      "project": 1,
      "created_at": "2025-02-17T12:00:00Z",
      "updated_at": "2025-02-17T12:00:00Z"
    },
    ...
  ]
}
```

### Testing

To test the API, you can use Postman or any other API testing tool to make requests to the endpoints listed above.

- **GET** `/api/tasks/` to list tasks.
- **POST** `/api/tasks/` to create a task (Admin only).
- **GET** `/api/tasks/{id}/` to get task details.
- **PATCH** `/api/tasks/{id}/` to update task status.
- **PUT** `/api/tasks/{id}/` to update a task.
- **DELETE** `/api/tasks/{id}/` to delete a task (Admin only).
